# System Architecture

## Overview

[Brief description of the system - what it does, who uses it]

## High-Level Structure

```
┌─────────────────────────────────────────────┐
│              User Interface                  │
│         (Web / Mobile / API)                 │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│           Application Layer                  │
│  (Business Logic, Services, Controllers)     │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│            Data Layer                        │
│     (Database, Cache, External APIs)         │
└─────────────────────────────────────────────┘
```

## Domain Boundaries

The system is divided into the following domains:

| Domain | Description | Owner |
|--------|-------------|-------|
| **Auth** | User authentication and authorization | [Team/Agent] |
| **Billing** | Payment processing and subscriptions | [Team/Agent] |
| **API** | External API endpoints | [Team/Agent] |
| **Admin** | Internal admin tools | [Team/Agent] |

Each domain follows the same layered structure (see below).

## Layered Architecture

Within each domain, code is organized into strict layers:

```
Domain/
├── types/       # TypeScript types, interfaces, schemas
├── config/      # Configuration, constants
├── repo/        # Data access layer (database queries)
├── service/     # Business logic
├── runtime/     # Runtime initialization, dependency injection
└── ui/          # UI components (if applicable)
```

**Dependency Rules:**
- Code can only depend "forward" (left to right in the list above)
- No circular dependencies allowed
- Cross-cutting concerns (auth, logging, metrics) accessed via `Providers` interface

**Example:**
```typescript
// ✅ GOOD: service depends on repo
import { getUserById } from '../repo/users';

// ❌ BAD: repo depends on service
import { validateUser } from '../service/validation';

// ✅ GOOD: Cross-cutting via Providers
import { logger } from '../runtime/providers';
```

## Technology Stack

### Core
- **Language:** TypeScript
- **Runtime:** Node.js 20+
- **Framework:** [Next.js / Express / etc.]

### Data
- **Database:** PostgreSQL
- **ORM:** Prisma
- **Cache:** Redis
- **Queue:** BullMQ

### Testing
- **Unit Tests:** Vitest
- **Integration Tests:** Playwright
- **E2E Tests:** Cypress

### Infrastructure
- **Hosting:** [AWS / Vercel / etc.]
- **CI/CD:** GitHub Actions
- **Monitoring:** [Datadog / Grafana / etc.]

## Key Design Decisions

### 1. Parse, Don't Validate
All external data (API requests, database results) must be validated at boundaries using Zod schemas.

```typescript
// ✅ GOOD
const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
});

const user = UserSchema.parse(apiResponse);
```

### 2. Shared Utilities
Common logic lives in shared packages, not duplicated across domains.

```typescript
// ✅ GOOD
import { retry } from '@/lib/utils/retry';

// ❌ BAD
function myRetry() { /* duplicated logic */ }
```

### 3. Structured Logging
All logs use structured format with context.

```typescript
// ✅ GOOD
logger.info({ userId, action: 'login' }, 'User logged in');

// ❌ BAD
console.log('User logged in');
```

## Architectural Constraints

These are enforced by custom linters and CI:

1. **No circular dependencies** - Detected by `madge`
2. **Layer violations** - Detected by custom ESLint rule
3. **Unvalidated data** - Detected by custom ESLint rule
4. **File size limit** - Max 300 lines per file
5. **Test coverage** - Min 80% for new code

## Diagrams

### Data Flow
```
User Request
    ↓
API Gateway
    ↓
Service Layer (validates, applies business logic)
    ↓
Repository Layer (queries database)
    ↓
Database
```

### Authentication Flow
```
[Add specific flow diagram]
```

### Deployment Architecture
```
[Add infrastructure diagram]
```

## Related Documentation

- [Design Principles](./principles.md)
- [API Documentation](./api.md)
- [Database Schema](./database.md)
- [Domain Documentation](./domains/)

---

**Last Updated:** [Date]  
**Maintained By:** [Team/Agent]
