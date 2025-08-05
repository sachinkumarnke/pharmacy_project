# How to Use Project Template JSON

## Purpose
This template helps you create documentation for any project that other AI systems can understand and recreate.

## Steps to Use:

### 1. Copy the Template
- Copy `project_template.json` to your new project folder
- Rename it to `project_documentation.json`

### 2. Replace Placeholders
Replace all `[PLACEHOLDER_TEXT]` with your actual project details:

**Example Replacements:**
- `[PROJECT_NAME]` → "My Blog Website"
- `[PROJECT_TYPE]` → "Django Web Application"
- `[BACKEND_TECHNOLOGY]` → "Django 4.2"
- `[DATABASE_TYPE]` → "SQLite"

### 3. Fill in Your Project Details

**For Django Projects:**
```json
"tech_stack": {
  "backend": "Django 4.2",
  "frontend": "HTML, CSS, Bootstrap",
  "database": "SQLite/PostgreSQL",
  "deployment": "Docker"
}
```

**For React Projects:**
```json
"tech_stack": {
  "backend": "Node.js/Express",
  "frontend": "React 18, CSS Modules",
  "database": "MongoDB",
  "deployment": "Vercel"
}
```

### 4. Document Your Models/Components
List all your database models or React components with their fields/props.

### 5. Add Your Features
Document each major feature with:
- Description
- Related files
- Functionality list

### 6. Include Setup Instructions
Write step-by-step instructions for:
- Installing dependencies
- Setting up environment
- Running the project

## Quick Example:

```json
{
  "project_info": {
    "name": "Todo App",
    "type": "React Web Application",
    "version": "1.0.0",
    "description": "Simple todo list with CRUD operations"
  },
  "database_models": {
    "Todo": {
      "fields": ["id", "title", "completed", "created_at"],
      "purpose": "Store todo items"
    }
  },
  "key_features": {
    "todo_management": {
      "description": "Add, edit, delete, mark complete todos",
      "files": ["TodoList.js", "TodoItem.js"],
      "functionality": ["Create todo", "Update todo", "Delete todo"]
    }
  }
}
```

## Benefits:
- **AI Understanding**: Other AI can recreate your project exactly
- **Documentation**: Serves as comprehensive project documentation  
- **Onboarding**: New developers understand project quickly
- **Maintenance**: Easy to track features and structure
- **Collaboration**: Share project knowledge efficiently

## Tips:
- Keep it updated when adding new features
- Be specific with file paths and names
- Include common issues in troubleshooting
- Add future enhancement ideas
- Use clear, descriptive language