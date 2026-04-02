# Golden Rules

These principles are mechanically enforced via linters, CI, and cleanup agents.

## 1. Parse, Don't Validate

**Rule:** Validate all external data at boundaries using schemas.

**Why:** Prevents runtime errors from malformed data.

**Enforcement:** Custom ESLint rule `no-unvalidated-api-data`

**Examples:**
```typescript
// ✅ GOOD
const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  age: z.number().min(0),
});

const user = UserSchema.parse(apiResponse);

// ❌ BAD
const user = apiResponse; // No validation
if (user.email.includes('@')) { // Validation scattered
  // ...
}
```

## 2. Shared Utilities Over Duplication

**Rule:** Use shared utility packages instead of duplicating logic.

**Why:** Centralizes invariants, easier to maintain.

**Enforcement:** Custom ESLint rule `prefer-shared-utils`

**Examples:**
```typescript
// ✅ GOOD
import { retry, sleep } from '@/lib/utils';

await retry(() => fetchData(), { maxAttempts: 3 });

// ❌ BAD
async function myRetry() {
  for (let i = 0; i < 3; i++) {
    try {
      return await fetchData();
    } catch (e) {
      await new Promise(r => setTimeout(r, 1000));
    }
  }
}
```

## 3. Structured Logging

**Rule:** Always use structured logging with context.

**Why:** Makes logs searchable and analyzable.

**Enforcement:** Custom ESLint rule `require-structured-logging`

**Examples:**
```typescript
// ✅ GOOD
logger.info({ userId, action: 'login', ip }, 'User logged in');
logger.error({ userId, error: err.message }, 'Login failed');

// ❌ BAD
console.log('User logged in');
console.log(`Error: ${err.message}`);
```

## 4. Type Safety

**Rule:** No `any` types without explicit justification.

**Why:** Maintains type safety benefits.

**Enforcement:** TypeScript strict mode + ESLint rule

**Examples:**
```typescript
// ✅ GOOD
function processUser(user: User): Result {
  // ...
}

// ✅ ACCEPTABLE (with comment)
// eslint-disable-next-line @typescript-eslint/no-explicit-any
function legacyAdapter(data: any): User {
  // Justification: Legacy API returns untyped data
  return UserSchema.parse(data);
}

// ❌ BAD
function processUser(user: any) {
  // ...
}
```

## 5. Test Coverage

**Rule:** Minimum 80% coverage for new code.

**Why:** Ensures reliability and prevents regressions.

**Enforcement:** CI check fails if coverage drops

**Examples:**
```typescript
// ✅ GOOD
describe('calculateTotal', () => {
  it('sums positive numbers', () => {
    expect(calculateTotal([1, 2, 3])).toBe(6);
  });
  
  it('handles empty array', () => {
    expect(calculateTotal([])).toBe(0);
  });
  
  it('handles negative numbers', () => {
    expect(calculateTotal([-1, 2])).toBe(1);
  });
});
```

## 6. Small Files

**Rule:** Maximum 300 lines per file.

**Why:** Keeps code readable and maintainable.

**Enforcement:** ESLint rule `max-lines`

**Solution:** Extract to separate modules or utilities.

## 7. No Circular Dependencies

**Rule:** No circular imports between modules.

**Why:** Causes initialization issues and tight coupling.

**Enforcement:** `madge` check in CI

**Examples:**
```typescript
// ❌ BAD
// a.ts
import { b } from './b';

// b.ts
import { a } from './a'; // Circular!

// ✅ GOOD
// Extract shared code to a third module
// shared.ts
export const shared = ...;

// a.ts
import { shared } from './shared';

// b.ts
import { shared } from './shared';
```

## 8. Layered Architecture

**Rule:** Code can only depend "forward" in the layer hierarchy.

**Why:** Maintains clear separation of concerns.

**Enforcement:** Custom structural tests

**Layers (in order):**
1. types
2. config
3. repo
4. service
5. runtime
6. ui

**Examples:**
```typescript
// ✅ GOOD
// service/users.ts
import { getUserById } from '../repo/users'; // service → repo

// ❌ BAD
// repo/users.ts
import { validateUser } from '../service/validation'; // repo → service (backward!)
```

## 9. Error Handling

**Rule:** Always handle errors explicitly, never silently swallow.

**Why:** Prevents silent failures and aids debugging.

**Enforcement:** ESLint rule `no-empty-catch`

**Examples:**
```typescript
// ✅ GOOD
try {
  await riskyOperation();
} catch (error) {
  logger.error({ error }, 'Operation failed');
  throw new AppError('Failed to complete operation', { cause: error });
}

// ❌ BAD
try {
  await riskyOperation();
} catch (error) {
  // Silent failure
}
```

## 10. Naming Conventions

**Rule:** Follow consistent naming patterns.

**Why:** Improves code readability and searchability.

**Enforcement:** Custom ESLint rules

**Conventions:**
- **Files:** `kebab-case.ts`
- **Classes:** `PascalCase`
- **Functions:** `camelCase`
- **Constants:** `UPPER_SNAKE_CASE`
- **Types/Interfaces:** `PascalCase`
- **Schemas:** `PascalCase` + `Schema` suffix

**Examples:**
```typescript
// ✅ GOOD
const MAX_RETRIES = 3;
class UserService {}
function calculateTotal() {}
const UserSchema = z.object({...});

// ❌ BAD
const maxRetries = 3; // Should be UPPER_SNAKE_CASE
class userService {} // Should be PascalCase
function CalculateTotal() {} // Should be camelCase
```

## Enforcement Tools

### Linters
```json
// .eslintrc.js
{
  "rules": {
    "no-unvalidated-api-data": "error",
    "prefer-shared-utils": "warn",
    "require-structured-logging": "error",
    "@typescript-eslint/no-explicit-any": "error",
    "max-lines": ["error", 300],
    "no-empty-catch": "error"
  }
}
```

### CI Checks
```yaml
# .github/workflows/quality.yml
- name: Check test coverage
  run: npm run test:coverage -- --threshold=80

- name: Check circular dependencies
  run: npx madge --circular src/

- name: Structural tests
  run: npm run test:structure
```

### Cleanup Agent
Runs daily to scan for violations and open refactoring PRs.

## Exceptions

Sometimes rules need to be broken. When that happens:

1. **Document why** in a comment
2. **Use ESLint disable** with justification
3. **Create a tech debt ticket** if it needs fixing later

```typescript
// eslint-disable-next-line @typescript-eslint/no-explicit-any
function legacyAdapter(data: any): User {
  // Justification: Legacy API returns untyped data
  // TODO: Add schema validation once API is updated
  return data as User;
}
```

---

**Last Updated:** [Date]  
**Maintained By:** cleanup-agent
