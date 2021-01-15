# 任务作业系统

- 脚本库相关
    - 项目管理
    - 脚本管理
    - 执行任务
    
## 一 项目管理
### 1.1 创建项目
```bash
URL: tasks/script-project/
Method: POST

请求: 
{
  "name": "项目名称",
  "path": "项目路径"
}
返回:
{
    "code": 2000,
    "message": "successful",
    "data": {
        "id": 1,
        "name": "测试路径",
        "path": "testxxxx",
        "latest_date": "2021-01-15 15:48:44",
        "create_date": "2021-01-15 15:48:44"
    }
}
```


