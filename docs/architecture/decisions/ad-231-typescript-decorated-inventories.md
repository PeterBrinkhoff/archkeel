# AD-231 TypeScript decorators retain direct lexical member inventories

A TypeScript member inventory certifies the statically named direct declarations
written in the classifier body. It excludes inherited and runtime-generated API.
Tree-sitter attaches field decorators to the field, but exposes method decorators
as preceding siblings in the class body. Treating those siblings as additional
unsupported members made valid method inventories partial, including NestJS's
otherwise complete `AppController` method scope.

Associate well-formed decorator siblings, allowing intervening decorators and
comments, with the following supported static member declaration. Do not count
the decorator as another lexical member. Preserve declaration names, spans,
signatures, lexical ownership and inventory IDs. Keep the existing parameter
property limit separate from this correction.

Publish actual decorator source spellings and their evidence IDs in the existing
symbol and attribute metadata. Recognize attached class decorators, including
decorators on the enclosing export statement, and attached field decorators.
The parsed decorated flag uses the same source association. These facts describe
syntax; they do not prove decorator dispatch, modified signatures or generated API.

Computed names, parser repairs, unsupported class-body blocks, dangling decorators
and unsupported constructor decoration keep inventories unclosed. Duplicate owners
retain ambiguous bindings. Quoted and escaped instance constructor names retain
the unsupported attachment; ordinary static methods and accessors named
`constructor` keep their source decorators. Complete direct scopes can prove declared presence,
known extra members and absent expected members. Partial scopes retain uncertainty
for absence while preserving known source declarations.

Native controls cover class, field and method decorators, multiple decorators and
comments, visibility, static methods, signatures, evidence and ownership, getters
and setters, unsupported attachments and ambiguous owners. Closed method and field
comparisons verify PASS and deliberate FAIL cases; fresh and saved reports agree.
The unchanged NestJS AppController is checked with its pinned external import input.
Source, Target intent, policy, budgets and schemas remain unchanged.
