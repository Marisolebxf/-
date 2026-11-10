/**
 * Small, dependency-free JSON Schema validator for the subset used by
 * .cursor/skills/feishu-bugfix/templates/state.schema.json.
 *
 * Supported: $ref, $defs, type, const, enum, oneOf, required, properties,
 * additionalProperties, items, minItems, minLength, minimum, maximum.
 */
function typeOf(value) {
  if (value === null) return 'null';
  if (Array.isArray(value)) return 'array';
  if (Number.isInteger(value)) return 'integer';
  return typeof value;
}

function matchesType(value, expected) {
  const actual = typeOf(value);
  if (expected === 'number') return actual === 'number' || actual === 'integer';
  return actual === expected;
}

function resolveRef(root, ref) {
  if (!ref.startsWith('#/')) throw new Error(`Unsupported $ref: ${ref}`);
  return ref.slice(2).split('/').reduce((node, part) => {
    if (!node || !(part in node)) throw new Error(`Unresolved $ref: ${ref}`);
    return node[part];
  }, root);
}

function validateNode(value, schema, root, path, errors) {
  if (schema === true || schema == null) return;
  if (schema === false) {
    errors.push(`${path}: schema forbids this value`);
    return;
  }
  if (schema.$ref) {
    validateNode(value, resolveRef(root, schema.$ref), root, path, errors);
    return;
  }
  if (schema.oneOf) {
    const branchResults = schema.oneOf.map((branch) => {
      const branchErrors = [];
      validateNode(value, branch, root, path, branchErrors);
      return branchErrors;
    });
    const passing = branchResults.filter((result) => result.length === 0).length;
    if (passing !== 1) {
      errors.push(`${path}: must match exactly one oneOf branch (matched ${passing})`);
      for (const [index, branchErrors] of branchResults.entries()) {
        if (branchErrors.length) errors.push(`${path}: oneOf[${index}] ${branchErrors.join('; ')}`);
      }
    }
    return;
  }
  if (schema.const !== undefined && value !== schema.const) {
    errors.push(`${path}: must equal ${JSON.stringify(schema.const)}`);
  }
  if (schema.enum && !schema.enum.some((candidate) => candidate === value)) {
    errors.push(`${path}: must be one of ${schema.enum.map((v) => JSON.stringify(v)).join(', ')}`);
  }
  if (schema.type) {
    const expected = Array.isArray(schema.type) ? schema.type : [schema.type];
    if (!expected.some((type) => matchesType(value, type))) {
      errors.push(`${path}: expected type ${expected.join('|')}, got ${typeOf(value)}`);
      return;
    }
  }
  if (typeof value === 'string') {
    if (schema.minLength != null && value.length < schema.minLength) {
      errors.push(`${path}: length must be >= ${schema.minLength}`);
    }
  }
  if (typeof value === 'number') {
    if (schema.minimum != null && value < schema.minimum) errors.push(`${path}: must be >= ${schema.minimum}`);
    if (schema.maximum != null && value > schema.maximum) errors.push(`${path}: must be <= ${schema.maximum}`);
  }
  if (Array.isArray(value)) {
    if (schema.minItems != null && value.length < schema.minItems) errors.push(`${path}: must contain >= ${schema.minItems} items`);
    if (schema.items) value.forEach((item, index) => validateNode(item, schema.items, root, `${path}[${index}]`, errors));
  }
  if (value && typeof value === 'object' && !Array.isArray(value)) {
    for (const key of schema.required ?? []) {
      if (!(key in value)) errors.push(`${path}.${key}: required property missing`);
    }
    const properties = schema.properties ?? {};
    for (const [key, child] of Object.entries(value)) {
      if (properties[key]) {
        validateNode(child, properties[key], root, `${path}.${key}`, errors);
      } else if (schema.additionalProperties === false) {
        errors.push(`${path}.${key}: additional property is forbidden`);
      } else if (schema.additionalProperties && typeof schema.additionalProperties === 'object') {
        validateNode(child, schema.additionalProperties, root, `${path}.${key}`, errors);
      }
    }
  }
}

export function validateJsonSchema(value, schema) {
  const errors = [];
  validateNode(value, schema, schema, '$', errors);
  return errors;
}
