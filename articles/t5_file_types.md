<table style="width: 100%;"><tr><td style="width: 40%;">
<a href="../articles/t5_files.md">Файлы.
</a></td><td style="width: 20%;">
<a href="../readme.md">Содержание
</a></td><td style="width: 40%;">
<a href="../articles/t5_file_types.md">Типы файлов.
</a></td><tr></table>

## CSV

<!-- https://docs.microsoft.com/en-us/dotnet/api/microsoft.visualbasic.fileio.textfieldparser?redirectedfrom=MSDN&view=net-5.0 -->

Парсер CSV теперь является частью фреймворка .NET.

Добавьте ссылку на Microsoft.VisualBasic.dll (отлично работает в C#,, не обращайте внимания на название)

```cs
using (TextFieldParser parser = new TextFieldParser(@"c:\temp\test.csv"))
{
    parser.TextFieldType = FieldType.Delimited;
    parser.SetDelimiters(",");
    while (!parser.EndOfData)
    {
        //Process row
        string[] fields = parser.ReadFields();
        foreach (string field in fields)
        {
            //TODO: Process field
        }
    }
}
```

## XML

