def get_file_name(request):
    file_name = request.get('file_name', '')
    print(file_name)
    if file_name == '':
        return 'file_name 参数必须传递.', False
    elif file_name.startswith(('.', '/', '$', '#')):
        return '文件名格式不正确.', False
    return file_name, True

