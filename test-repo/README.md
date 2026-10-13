# ASTRA Target Test Repository

This directory will contain the separate JavaScript/Node.js repository that ASTRA will inspect and operate on during the first prototype.

It is deliberately separate from `astra-system/` so ASTRA can be tested as an external engineering system instead of receiving special access to its own source code.

The first target contains an intentionally failing test and a bounded task that ASTRA must investigate, plan, modify and verify.

## Current structure

```text
test-repo/
├── server/
│   ├── controllers/
│   ├── models/
│   ├── repositories/
│   └── services/
├── test/
└── package.json
```

The current flow is:

```text
Controller -> Service -> Repository -> Model
```

Here, `repository` means the application data-access layer. It is different from the GitHub repository that contains the project.

## Seeded engineering task

Expected behavior: after a task is completed, it must not appear in the pending-task list.

The test currently fails intentionally. ASTRA will later be given this failure as its first bounded engineering task.

Run the baseline test with:

```powershell
npm.cmd test
```
