# Sprint Planning Template

## Sprint Overview
**Sprint**: [Sprint Number/Name]
**Duration**: [Start Date] - [End Date]
**Story Points**: [Total Points]

## Objectives
1. [Primary sprint goal]
2. [Secondary objectives]

## User Stories
### [Story Title]
- **ID**: [Story ID]
- **Points**: [Story Points]
- **Priority**: [High/Medium/Low]
- **Description**:
  ```
  As a [user type]
  I want to [action]
  So that [benefit]
  ```
- **Acceptance Criteria**:
  - [ ] Criterion 1
  - [ ] Criterion 2

## Technical Tasks
### [Task Title]
- **Related Story**: [Story ID]
- **Assignee**: [Name]
- **Estimated Hours**: [Hours]
- **Dependencies**:
  - [Task/Story IDs]
- **Subtasks**:
  - [ ] Subtask 1
  - [ ] Subtask 2

## Timeline
```mermaid
%%{
  init: {
    'theme': 'base',
    'themeVariables': {
      'primaryColor': '#326CE5',
      'primaryTextColor': '#fff',
      'primaryBorderColor': '#114BB7',
      'lineColor': '#114BB7',
      'secondaryColor': '#6C8EBF',
      'tertiaryColor': '#82B366'
    },
    'gantt': {
      'titleTopMargin': 25,
      'barHeight': 30,
      'barGap': 8,
      'topPadding': 40,
      'bottomPadding': 40,
      'leftPadding': 100,
      'rightPadding': 100,
      'fontSize': '14px'
    }
  }
}%%
gantt
    title Sprint Timeline
    dateFormat YYYY-MM-DD
    axisFormat %d-%b
    excludes weekends
    
    section User Story 1
    Task Planning     :done, t1, 2024-01-01, 1d
    Development      :active, t2, after t1, 3d
    Code Review      :t3, after t2, 1d
    Testing         :t4, after t3, 2d
    
    section User Story 2
    Task Planning     :done, t5, 2024-01-02, 1d
    Development      :t6, after t5, 4d
    Code Review      :t7, after t6, 1d
    
    section User Story 3
    Task Planning     :t8, 2024-01-03, 1d
    Development      :t9, after t8, 3d
    Testing         :t10, after t9, 2d
```

## Risk Assessment
| Risk | Impact | Mitigation |
|------|--------|------------|
| Risk 1 | High/Med/Low | Strategy |

## Resources
- **Team Members**:
  - [Name]: [Role]
- **External Dependencies**:
  - [Dependency]: [Status]

## Definition of Done
- [ ] Code reviewed
- [ ] Tests written and passing
- [ ] Documentation updated
- [ ] Deployed to staging
- [ ] Product owner approval

## Metrics
- [ ] Velocity target
- [ ] Quality metrics
- [ ] Technical debt addressed

## Notes
- Sprint planning notes
- Technical decisions
- Dependencies
