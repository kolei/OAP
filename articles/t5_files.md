Предыдущая лекция | &nbsp; | Следующая лекция
:----------------:|:----------:|:----------------:
[Исключения. Null.](./t5_exception.md) | [Содержание](../readme.md#тема-5-продвинутый-c-функции-лямбды-исключения-работа-с-файлами-многопоточность-регулярные-выражения) | [Многопоточность. Потоки, асинхронные вычисления](./t5_thread_async.md)

# Работа с потоками и файловой системой

Большинство задач в программировании так или иначе связаны с работой с файлами и каталогами. Нам может потребоваться прочитать текст из файла или наоборот произвести запись, удалить файл или целый каталог, не говоря уже о более комплексных задачах, как например, создание текстового редактора и других подобных задачах.

Фреймворк .NET предоставляет большие возможности по управлению и манипуляции файлами и каталогами, которые по большей части сосредоточены в пространстве имен `System.IO`. Классы, расположенные в этом пространстве имен (такие как **Stream**, **StreamWriter**, **FileStream** и др.), позволяют управлять файловым вводом-выводом.

## Работа с дисками

Работу с файловой системой начнем с самого верхнего уровня - дисков. Для представления диска в пространстве имен `System.IO` имеется класс **DriveInfo**.

Этот класс имеет статический метод _GetDrives_, который возвращает имена всех логических дисков компьютера. Также он предоставляет ряд полезных свойств:

* *AvailableFreeSpace*: указывает на объем доступного свободного места на диске в байтах
* *DriveFormat*: получает имя файловой системы
* *DriveType*: представляет тип диска
* *IsReady*: готов ли диск (например, DVD-диск может быть не вставлен в дисковод)
* *Name*: получает имя диска
* *TotalFreeSpace*: получает общий объем свободного места на диске в байтах
* *TotalSize*: общий размер диска в байтах
* *VolumeLabel*: получает или устанавливает метку тома

Получим имена и свойства всех дисков на компьютере:

```cs
using System;
using System.IO;
 
DriveInfo[] drives = DriveInfo.GetDrives();

foreach (DriveInfo drive in drives)
{
    Console.WriteLine($"Название: {drive.Name}");
    Console.WriteLine($"Тип: {drive.DriveType}");
    if (drive.IsReady)
    {
        Console.WriteLine($"Объем диска: {drive.TotalSize}");
        Console.WriteLine($"Свободное пространство: {drive.TotalFreeSpace}");
        Console.WriteLine($"Метка: {drive.VolumeLabel}");
    }
    Console.WriteLine();
}
```

```
Название: C:\
Тип: Fixed
Объем диска: 63757606912
Свободное пространство: 13795221504
Метка:

Название: D:\
Тип: CDRom
```

## Работа с каталогами

Для работы с каталогами в пространстве имен `System.IO` предназначены сразу два класса: **Directory** и **DirectoryInfo**.

### Класс **Directory**

Класс **Directory** предоставляет ряд статических методов для управления каталогами. Некоторые из этих методов:

* *CreateDirectory(path)*: создает каталог по указанному пути path
* *Delete(path)*: удаляет каталог по указанному пути path
* *Exists(path)*: определяет, существует ли каталог по указанному пути path. Если существует, возвращается true, если не существует, то false
* *GetDirectories(path)*: получает список каталогов в каталоге path
* *GetFiles(path)*: получает список файлов в каталоге path
* *Move(sourceDirName, destDirName)*: перемещает каталог
* *GetParent(path)*: получение родительского каталога

### Класс **DirectoryInfo**

Данный класс предоставляет функциональность для создания, удаления, перемещения и других операций с каталогами. Во многом он похож на **Directory**. Некоторые из его свойств и методов:

* *Create()*: создает каталог
* *CreateSubdirectory(path)*: создает подкаталог по указанному пути path
* *Delete()*: удаляет каталог
* Свойство *Exists*: определяет, существует ли каталог
* *GetDirectories()*: получает список каталогов
* *GetFiles()*: получает список файлов
* *MoveTo(destDirName)*: перемещает каталог
* Свойство *Parent*: получение родительского каталога
* Свойство *Root*: получение корневого каталога

Посмотрим на примерах применение этих классов

#### Получение списка файлов и подкаталогов

```cs
string dirName = "C:\\";
 
if (Directory.Exists(dirName))
{
    Console.WriteLine("Подкаталоги:");
    string[] dirs = Directory.GetDirectories(dirName);
    foreach (string s in dirs)
    {
        Console.WriteLine(s);
    }
    Console.WriteLine();
    Console.WriteLine("Файлы:");
    string[] files = Directory.GetFiles(dirName);
    foreach (string s in files)
    {
        Console.WriteLine(s);
    }
}
```

Обратите внимание на использование слешей в именах файлов. Либо мы используем двойной слеш: `C:\\`, либо одинарный, но тогда перед строкой ставим знак `@`: `@"C:\Program Files"`

>Можно вместо обратных слешей использовать прямые. Windows нормально их воспринимает

#### Создание каталога

```cs
string path = @"C:\SomeDir";
string subpath = @"program\avalon";
DirectoryInfo dirInfo = new DirectoryInfo(path);
if (!dirInfo.Exists)
{
    dirInfo.Create();
}
dirInfo.CreateSubdirectory(subpath);
```

Вначале проверяем, а нет ли такой директории, так как если она существует, то ее создать будет нельзя, и приложение выбросит ошибку. В итоге у нас получится следующий путь: `C:\SomeDir\program\avalon`

#### Получение информации о каталоге

```cs
string dirName = "C:\\Program Files";
 
DirectoryInfo dirInfo = new DirectoryInfo(dirName);
 
Console.WriteLine($"Название каталога: {dirInfo.Name}");
Console.WriteLine($"Полное название каталога: {dirInfo.FullName}");
Console.WriteLine($"Время создания каталога: {dirInfo.CreationTime}");
Console.WriteLine($"Корневой каталог: {dirInfo.Root}");
```

#### Удаление каталога

Если мы просто применим метод _Delete_ к непустой папке, в которой есть какие-нибудь файлы или подкаталоги, то приложение нам выбросит ошибку. Поэтому нам надо передать в метод _Delete_ дополнительный параметр булевого типа, который укажет, что папку надо удалять со всем содержимым:

```cs
string dirName = @"C:\SomeFolder";
 
try
{
    DirectoryInfo dirInfo = new DirectoryInfo(dirName);
    dirInfo.Delete(true);
    Console.WriteLine("Каталог удален");
}
catch (Exception ex)
{
    Console.WriteLine(ex.Message);
}
```

Или так:

```cs
string dirName = @"C:\SomeFolder";
 
Directory.Delete(dirName, true);
```

#### Перемещение каталога

```cs
string oldPath = @"C:\SomeFolder";
string newPath = @"C:\SomeDir";
DirectoryInfo dirInfo = new DirectoryInfo(oldPath);
if (dirInfo.Exists && Directory.Exists(newPath) == false)
{
    dirInfo.MoveTo(newPath);
}
```

При перемещении надо учитывать, что новый каталог, в который мы хотим перемесить все содержимое старого каталога, не должен существовать.

## Работа с файлами. Классы **File** и **FileInfo**

Подобно паре **Directory**/**DirectoryInfo** для работы с файлами предназначена пара классов **File** и **FileInfo**. С их помощью мы можем создавать, удалять, перемещать файлы, получать их свойства и многое другое.

Некоторые полезные методы и свойства класса **FileInfo**:

* *CopyTo(path)*: копирует файл в новое место по указанному пути path
* *Create()*: создает файл
* *Delete()*: удаляет файл
* *MoveTo(destFileName)*: перемещает файл в новое место
* Свойство *Directory*: получает родительский каталог в виде объекта DirectoryInfo
* Свойство *DirectoryName*: получает полный путь к родительскому каталогу
* Свойство *Exists*: указывает, существует ли файл
* Свойство *Length*: получает размер файла
* Свойство *Extension*: получает расширение файла
* Свойство *Name*: получает имя файла
* Свойство *FullName*: получает полное имя файла

Класс **File** реализует похожую функциональность с помощью статических методов:

* *Copy()*: копирует файл в новое место
* *Create()*: создает файл
* *Delete()*: удаляет файл
* *Move*: перемещает файл в новое место
* *Exists(file)*: определяет, существует ли файл

### Получение информации о файле

```cs
string path = @"C:\apache\hta.txt";
FileInfo fileInf = new FileInfo(path);
if (fileInf.Exists)
{
    Console.WriteLine("Имя файла: {0}", fileInf.Name);
    Console.WriteLine("Время создания: {0}", fileInf.CreationTime);
    Console.WriteLine("Размер: {0}", fileInf.Length);
}
```

### Удаление файла

```cs
string path = @"C:\apache\hta.txt";
FileInfo fileInf = new FileInfo(path);
if (fileInf.Exists)
{
   fileInf.Delete();
   // альтернатива с помощью класса File
   // File.Delete(path);
}
```

### Перемещение файла

```cs
string path = @"C:\apache\hta.txt";
string newPath = @"C:\SomeDir\hta.txt";
FileInfo fileInf = new FileInfo(path);
if (fileInf.Exists)
{
   fileInf.MoveTo(newPath);       
   // альтернатива с помощью класса File
   // File.Move(path, newPath);
}
```

### Копирование файла

```cs
string path = @"C:\apache\hta.txt";
string newPath = @"C:\SomeDir\hta.txt";
FileInfo fileInf = new FileInfo(path);
if (fileInf.Exists)
{
   fileInf.CopyTo(newPath, true);      
   // альтернатива с помощью класса File
   // File.Copy(path, newPath, true);
}
```

Метод *CopyTo* класса **FileInfo** принимает два параметра: путь, по которому файл будет копироваться, и булевое значение, которое указывает, надо ли при копировании перезаписывать файл (если **true**, как в случае выше, файл при копировании перезаписывается). Если же в качестве последнего параметра передать значение **false**, то если такой файл уже существует, приложение выдаст ошибку.

Метод *Copy* класса **File** принимает три параметра: путь к исходному файлу, путь, по которому файл будет копироваться, и булевое значение, указывающее, будет ли файл перезаписываться.

## **FileStream**. Чтение и запись файла

Класс **FileStream** представляет возможности по считыванию из файла и записи в файл. Он позволяет работать как с текстовыми файлами, так и с бинарными.

### Создание **FileStream**

Для создания объекта **FileStream** можно использовать как конструкторы этого класса, так и статические методы класса **File**. Конструктор **FileStream** имеет множество перегруженных версий, из которых отмечу лишь одну, самую простую и используемую:

```cs
FileStream(string filename, FileMode mode)
```

Здесь в конструктор передается два параметра: путь к файлу и перечисление (**enum**) *FileMode*. Данное перечисление указывает на режим доступа к файлу и может принимать следующие значения:

* *Append*: если файл существует, то текст добавляется в конец файл. Если файла нет, то он создается. Файл открывается только для записи.
* *Create*: создается новый файл. Если такой файл уже существует, то он перезаписывается
* *CreateNew*: создается новый файл. Если такой файл уже существует, то он приложение выбрасывает ошибку
* *Open*: открывает файл. Если файл не существует, выбрасывается исключение
* *OpenOrCreate*: если файл существует, он открывается, если нет - создается новый
* *Truncate*: если файл существует, то он перезаписывается. Файл открывается только для записи.

Другой способ создания объекта *FileStream* представляют статические методы класса *File*:

```cs
FileStream File.Open(string file, FileMode mode);
FileStream File.OpenRead(string file);
FileStream File.OpenWrite(string file);
```

Первый метод открывает файл с учетом объекта *FileMode* и возвращает файловой поток **FileStream**. У этого метода также есть несколько перегруженных версий. Второй метод открывает поток для чтения, а третий открывает поток для записи.

### Свойства и методы **FileStream**

Рассмотрим наиболее важные его свойства и методы класса **FileStream**:

* Свойство *Length*: возвращает длину потока в байтах
* Свойство *Position*: возвращает текущую позицию в потоке
* *void CopyTo(Stream destination)*: копирует данные из текущего потока в поток destination
* *Task CopyToAsync(Stream destination)*: асинхронная версия метода CopyToAsync
* *int Read(byte[] array, int offset, int count)*: считывает данные из файла в массив байтов и возвращает количество успешно считанных байтов. Принимает три параметра:

    * *array* - массив байтов, куда будут помещены считываемые из файла данные

    * *offset* представляет смещение в байтах в массиве array, в который считанные байты будут помещены

    * *count* - максимальное число байтов, предназначенных для чтения. Если в файле находится меньшее количество байтов, то все они будут считаны.

* `Task<int> ReadAsync(byte[] array, int offset, int count)`: асинхронная версия метода Read

* `long Seek(long offset, SeekOrigin origin)`: устанавливает позицию в потоке со смещением на количество байт, указанных в параметре *offset*.

* `void Write(byte[] array, int offset, int count)`: записывает в файл данные из массива байтов. Принимает три параметра:

    * *array* - массив байтов, откуда данные будут записываться в файл

    * *offset* - смещение в байтах в массиве array, откуда начинается запись байтов в поток

    * *count* - максимальное число байтов, предназначенных для записи

* `ValueTask WriteAsync(byte[] array, int offset, int count)`: асинхронная версия метода Write

### Чтение и запись файлов

**FileStream** представляет доступ к файлам на уровне байтов, поэтому, например, если вам надо считать или записать одну или несколько строк в текстовый файл, то массив байтов надо преобразовать в строки, используя специальные методы. Поэтому для работы с текстовыми файлами применяются другие классы.

В то же время при работе с различными бинарными файлами, имеющими определенную структуру, **FileStream** может быть очень даже полезен для извлечения определенных порций информации и ее обработки.

Посмотрим на примере считывания-записи в текстовый файл:

```cs
using System;
using System.IO;
 
namespace HelloApp
{
    class Program
    {
        static void Main(string[] args)
        {
            // создаем каталог для файла
            string path = @"C:\SomeDir2";
            DirectoryInfo dirInfo = new DirectoryInfo(path);
            if (!dirInfo.Exists)
            {
                dirInfo.Create();
            }
            Console.WriteLine("Введите строку для записи в файл:");
            string text = Console.ReadLine();
 
            // запись в файл
            using (FileStream fstream = new FileStream($"{path}\note.txt", FileMode.OpenOrCreate))
            {
                // преобразуем строку в байты
                byte[] array = System.Text.Encoding.Default.GetBytes(text);
                // запись массива байтов в файл
                fstream.Write(array, 0, array.Length);
                Console.WriteLine("Текст записан в файл");
            }
 
            // чтение из файла
            using (FileStream fstream = File.OpenRead($"{path}\note.txt"))
            {
                // преобразуем строку в байты
                byte[] array = new byte[fstream.Length];
                // считываем данные
                fstream.Read(array, 0, array.Length);
                // декодируем байты в строку
                string textFromFile = System.Text.Encoding.Default.GetString(array);
                Console.WriteLine($"Текст из файла: {textFromFile}");
            }
 
            Console.ReadLine();
        }
    }
}
``` 

Разберем этот пример. Вначале создается папка для файла. Кроме того, на уровне операционной системы могут быть установлены ограничения на запись в определенных каталогах, и при попытке создания и записи файла в подобных каталогах мы получим ошибку.

И при чтении, и при записи используется оператор **using**. Не надо путать данный оператор с директивой **using**, которая подключает пространства имен в начале файла кода. Оператор **using** позволяет создавать объект в блоке кода, по завершению которого вызывается метод *Dispose* у этого объекта, и, таким образом, объект уничтожается. В данном случае в качестве такого объекта служит переменная *fstream*.

И при записи, и при чтении применяется объект кодировки `Encoding.Default` из пространства имен `System.Text`. В данном случае мы используем два его метода: *GetBytes* для получения массива байтов из строки и *GetString* для получения строки из массива байтов.

В итоге введенная нами строка записывается в файл `note.txt`. По сути это бинарный файл (не текстовый), хотя если мы в него запишем только строку, то сможем посмотреть в удобочитаемом виде этот файл, открыв его в текстовом редакторе. Однако если мы в него запишем случайные байты, например:

```cs
fstream.WriteByte(13);
fstream.WriteByte(103);
```

То у нас могут возникнуть проблемы с его пониманием. Поэтому для работы непосредственно с текстовыми файлами предназначены отдельные классы - *StreamReader* и *StreamWriter*.

В реальных приложениях рекомендуется использовать асинхронные версии методов **FileStream**, поскольку операции с файлами могут занимать продолжительное время и являются узким местом в работе программы. Например, изменим выше приведенную программу, применив асинхронные методы:

```cs
using System;
using System.IO;
using System.Threading.Tasks;
 
namespace HelloApp
{
    class Program
    {
        static async Task Main(string[] args)
        {
            // создаем каталог для файла
            string path = @"C:\SomeDir3";
            DirectoryInfo dirInfo = new DirectoryInfo(path);
            if (!dirInfo.Exists)
            {
                dirInfo.Create();
            }
            Console.WriteLine("Введите строку для записи в файл:");
            string text = Console.ReadLine();
 
            // запись в файл
            using (FileStream fstream = new FileStream($"{path}\note.txt", FileMode.OpenOrCreate))
            {
                byte[] array = System.Text.Encoding.Default.GetBytes(text);
                // асинхронная запись массива байтов в файл
                await fstream.WriteAsync(array, 0, array.Length);
                Console.WriteLine("Текст записан в файл");
            }
 
            // чтение из файла
            using (FileStream fstream = File.OpenRead($"{path}\note.txt"))
            {
                byte[] array = new byte[fstream.Length];
                // асинхронное чтение файла
                await fstream.ReadAsync(array, 0, array.Length);
 
                string textFromFile = System.Text.Encoding.Default.GetString(array);
                Console.WriteLine($"Текст из файла: {textFromFile}");
            }
 
            Console.ReadLine();
        }
    }
}
```

### Произвольный доступ к файлам

Нередко бинарные файлы представляют определенную структуру. И, зная эту структуру, мы можем взять из файла нужную порцию информации или наоброт записать в определенном месте файла определенный набор байтов. Например, в wav-файлах непосредственно звуковые данные начинаются с 44 байта, а до 44 байта идут различные метаданные - количество каналов аудио, частота дискретизации и т.д.

С помощью метода *Seek* мы можем управлять положением курсора потока, начиная с которого производится считывание или запись в файл. Этот метод принимает два параметра: *offset* (смещение) и позиция в файле. Позиция в файле описывается тремя значениями:

* `SeekOrigin.Begin`: начало файла
* `SeekOrigin.End`: конец файла
* `SeekOrigin.Current`: текущая позиция в файле

Курсор потока, с которого начинается чтение или запись, смещается вперед на значение *offset* относительно позиции, указанной в качестве второго параметра. Смещение может быть отрицательным, тогда курсор сдвигается назад, если положительное - то вперед.

Рассмотрим на примере:

```cs
using System.IO;
using System.Text;
 
class Program
{
    static void Main(string[] args)
    {
        string text = "hello world";
             
        // запись в файл
        using (FileStream fstream = new FileStream(@"D:\note.dat", FileMode.OpenOrCreate))
        {
            // преобразуем строку в байты
            byte[] input = Encoding.Default.GetBytes(text);
            // запись массива байтов в файл
            fstream.Write(input, 0, input.Length);
            Console.WriteLine("Текст записан в файл");
 
            // перемещаем указатель в конец файла, до конца файла- пять байт
            fstream.Seek(-5, SeekOrigin.End); // минус 5 символов с конца потока
 
            // считываем четыре символов с текущей позиции
            byte[] output = new byte[4];
            fstream.Read(output, 0, output.Length);
            // декодируем байты в строку
            string textFromFile = Encoding.Default.GetString(output);
            Console.WriteLine($"Текст из файла: {textFromFile}"); // worl
 
            // заменим в файле слово world на слово house
            string replaceText = "house";
            fstream.Seek(-5, SeekOrigin.End); // минус 5 символов с конца потока
            input = Encoding.Default.GetBytes(replaceText);
            fstream.Write(input, 0, input.Length);
 
            // считываем весь файл
            // возвращаем указатель в начало файла
            fstream.Seek(0, SeekOrigin.Begin);
            output = new byte[fstream.Length];
            fstream.Read(output, 0, output.Length);
            // декодируем байты в строку
            textFromFile = Encoding.Default.GetString(output);
            Console.WriteLine($"Текст из файла: {textFromFile}"); // hello house
        }
        Console.Read();
    }
}
```

Консольный вывод:

```
Текст записан в файл
Текст из файла: worl
Текст из файла: hello house
```

Вызов `fstream.Seek(-5, SeekOrigin.End)` перемещает курсор потока в конец файлов назад на пять символов:

![](../img/05002.png)

То есть после записи в новый файл строки "hello world" курсор будет стоять на позиции символа "w".

После этого считываем четыре байта начиная с символа "w". В данной кодировке один символ будет представлять один байт. Поэтому чтение 4-х байтов будет эквивалентно чтению четырех сиволов: "worl".

Затем опять же перемещаемся в конец файла, не доходя до конца пять символов (то есть опять же с позиции символа "w"), и осуществляем запись строки "house". Таким образом, строка "house" заменяет строку "world".

### Закрытие потока

В примерах выше для закрытия потока применяется конструкция **using**. После того как все операторы и выражения в блоке **using** отработают, объект **FileStream** уничтожается. Однако мы можем выбрать и другой способ:

```cs
FileStream fstream = null;
try
{
    fstream = new FileStream(@"D:\note3.dat", FileMode.OpenOrCreate);
    // операции с потоком
}
catch(Exception ex)
{
 
}
finally
{
    if (fstream != null)
        fstream.Close();
}
```

Если мы не используем конструкцию **using**, то нам надо явным образом вызвать метод *Close*: `fstream.Close()`

### Чтение и запись текстовых файлов. StreamReader и StreamWriter

Класс **FileStream** не очень удобно применять для работы с текстовыми файлами. Для этого в пространстве `System.IO` определены специальные классы: **StreamReader** и **StreamWriter**.

#### Запись в файл и **StreamWriter**

Для записи в текстовый файл используется класс **StreamWriter**. Некоторые из его конструкторов, которые могут применяться для создания объекта **StreamWriter**:

* `StreamWriter(string path)`: через параметр _path_ передается путь к файлу, который будет связан с потоком

* `StreamWriter(string path, bool append)`: параметр _append_ указывает, надо ли добавлять в конец файла данные или же перезаписывать файл. Если равно **true**, то новые данные добавляются в конец файла. Если равно **false**, то файл перезаписываетсяя заново

* `StreamWriter(string path, bool append, System.Text.Encoding encoding)`: параметр *encoding* указывает на кодировку, которая будет применяться при записи

Свою функциональность **StreamWriter** реализует через следующие методы:

* `int Close()`: закрывает записываемый файл и освобождает все ресурсы

* `void Flush()`: записывает в файл оставшиеся в буфере данные и очищает буфер.

* `Task FlushAsync()`: асинхронная версия метода _Flush_

* `void Write(string value)`: записывает в файл данные простейших типов, как **int**, **double**, **char**, **string** и т.д. Соответственно имеет ряд перегруженных версий для записи данных элементарных типов, например, `Write(char value)`, `Write(int value)`, `Write(double value)` и т.д.

* `Task WriteAsync(string value)`: асинхронная версия метода _Write_

* `void WriteLine(string value)`: также записывает данные, только после записи добавляет в файл символ окончания строки

* `Task WriteLineAsync(string value)`: асинхронная версия метода *WriteLine*

Рассмотрим запись в файл на примере:

```cs
using System;
using System.IO;
 
namespace HelloApp
{
    class Program
    {
        static void Main(string[] args)
        {
            string writePath = @"C:\SomeDir\hta.txt";
 
            string text = "Привет мир!\nПока мир...";
            try
            {
                using (StreamWriter sw = new StreamWriter(
                    writePath, false, System.Text.Encoding.Default))
                {
                    sw.WriteLine(text);
                }
 
                using (StreamWriter sw = new StreamWriter(
                    writePath, true, System.Text.Encoding.Default))
                {
                    sw.WriteLine("Дозапись");
                    sw.Write(4.5);
                }
                Console.WriteLine("Запись выполнена");
            }
            catch (Exception e)
            {
                Console.WriteLine(e.Message);
            }
        }
    }
}
```

В данном случае два раза создаем объект **StreamWriter**. В первом случае если файл существует, то он будет перезаписан. Если не существует, он будет создан. И в нее будет записан текст из переменной *text*. Во втором случае файл открывается для дозаписи, и будут записаны атомарные данные - строка и число. В обоих случаях будет использоваться кодировка по умолчанию.

По завершении программы в папке `C:/SomeDir` мы сможем найти файл `hta.txt`, который будет иметь следующие строки:

```
Привет мир!
Пока мир...
Дозапись
4,5
```

Поскольку операции с файлами могут занимать продолжительное время, то в общем случае рекомендуется использовать асинхронную запись. Используем асинхронные версии методов:

```cs
using System;
using System.IO;
using System.Threading.Tasks;
 
namespace HelloApp
{
    class Program
    {
        static async Task Main(string[] args)
        {
            string writePath = @"C:\SomeDir\hta2.txt";
 
            string text = "Привет мир!\nПока мир...";
            try
            {
                using (StreamWriter sw = new StreamWriter(
                    writePath, false, System.Text.Encoding.Default))
                {
                    await sw.WriteLineAsync(text);
                }
 
                using (StreamWriter sw = new StreamWriter(
                    writePath, true, System.Text.Encoding.Default))
                {
                    await sw.WriteLineAsync("Дозапись");
                    await sw.WriteAsync("4,5");
                }
                Console.WriteLine("Запись выполнена");
            }
            catch (Exception e)
            {
                Console.WriteLine(e.Message);
            }
        }
    }
}
```

Обратите внимание, что асинхронные версии есть не для всех перегрузок метода *Write*.

#### Чтение из файла и **StreamReader**

Класс **StreamReader** позволяет нам легко считывать весь текст или отдельные строки из текстового файла.

Некоторые из конструкторов класса **StreamReader**:

* `StreamReader(string path)`: через параметр _path_ передается путь к считываемому файлу

* `StreamReader(string path, System.Text.Encoding encoding)`: параметр _encoding_ задает кодировку для чтения файла

Среди методов **StreamReader** можно выделить следующие:

* `void Close()`: закрывает считываемый файл и освобождает все ресурсы

* `int Peek()`: возвращает следующий доступный символ, если символов больше нет, то возвращает `-1`

* `int Read()`: считывает и возвращает следующий символ в численном представлении. Имеет перегруженную версию: `Read(char[] array, int index, int count)`, где *array* - массив, куда считываются символы, *index* - индекс в массиве *array*, начиная с которого записываются считываемые символы, и *count* - максимальное количество считываемых символов

* `Task<int> ReadAsync()`: асинхронная версия метода *Read*

* `string ReadLine()`: считывает одну строку в файле

* `string ReadLineAsync()`: асинхронная версия метода _ReadLine_

* `string ReadToEnd()`: считывает весь текст из файла

* `string ReadToEndAsync()`: асинхронная версия метода _ReadToEnd_

Сначала считаем текст полностью из ранее записанного файла:

```cs
using System;
using System.IO;
using System.Threading.Tasks;
 
string path = @"C:\SomeDir\hta.txt";

try
{
    using (StreamReader sr = new StreamReader(path))
    {
        Console.WriteLine(sr.ReadToEnd());
    }
    // асинхронное чтение
    using (StreamReader sr = new StreamReader(path))
    {
        Console.WriteLine(await sr.ReadToEndAsync());
    }
}
catch (Exception e)
{
    Console.WriteLine(e.Message);
}
```

Считаем текст из файла построчно:

```cs
string path= @"C:\SomeDir\hta.txt";
   
using (StreamReader sr = new StreamReader(path, System.Text.Encoding.Default))
{
    string line;
    while ((line = sr.ReadLine()) != null)
    {
        Console.WriteLine(line);
    }
}
// асинхронное чтение
using (StreamReader sr = new StreamReader(path, System.Text.Encoding.Default))
{
    string line;
    while ((line = await sr.ReadLineAsync()) != null)
    {
        Console.WriteLine(line);
    }
}
```

В данном случае считываем построчно через цикл **while**: `while ((line = sr.ReadLine()) != null)` - сначала присваиваем переменной *line* результат функции `sr.ReadLine()`, а затем проверяем, не равна ли она **null**. Когда объект `sr` дойдет до конца файла и больше строк не останется, то метод `sr.ReadLine()` будет возвращать null.

## Бинарные файлы. **BinaryWriter** и **BinaryReader**

Для работы с бинарными файлами предназначена пара классов **BinaryWriter** и **BinaryReader**. Эти классы позволяют читать и записывать данные в двоичном формате.

Основные метода класса **BinaryWriter**

* `Close()`: закрывает поток и освобождает ресурсы

* `Flush()`: очищает буфер, дописывая из него оставшиеся данные в файл

* `Seek()`: устанавливает позицию в потоке

* `Write()`: записывает данные в поток

Основные метода класса **BinaryReader**

* `Close()`: закрывает поток и освобождает ресурсы

* `ReadBoolean()`: считывает значение **bool** и перемещает указатель на один байт

* *ReadByte()*: считывает один байт и перемещает указатель на один байт

* `ReadChar()`: считывает значение **char**, то есть один символ, и перемещает указатель на столько байтов, сколько занимает символ в текущей кодировке

* `ReadDecimal()`: считывает значение **decimal** и перемещает указатель на 16 байт

* `ReadDouble()`: считывает значение **double** и перемещает указатель на 8 байт

* `ReadInt16()`: считывает значение **short** и перемещает указатель на 2 байта

* `ReadInt32()`: считывает значение **int** и перемещает указатель на 4 байта

* `ReadInt64()`: считывает значение **long** и перемещает указатель на 8 байт

* `ReadSingle()`: считывает значение *float* и перемещает указатель на 4 байта

* `ReadString()`: считывает значение **string**. Каждая строка предваряется значением длины строки, которое представляет 7-битное целое число

С чтением бинарных данных все просто: соответствующий метод считывает данные определенного типа и перемещает указатель на размер этого типа в байтах, например, значение типа **int** занимает 4 байта, поэтому **BinaryReader** считает 4 байта и переместит указать на эти 4 байта.

Посмотрим на реальной задаче применение этих классов. Попробуем с их помощью записывать и считывать из файла массив структур:

```cs
struct State
{
    public string name;
    public string capital;
    public int area;
    public double people;
 
    public State(string n, string c, int a, double p)
    {
        name = n;
        capital = c;
        people = p;
        area = a;
    }
}
class Program
{
    static void Main(string[] args)
    {
        State[] states = new State[2];
        states[0] = new State("Германия", "Берлин",  357168,  80.8);
        states[1] = new State("Франция", "Париж", 640679, 64.7);
 
        string path= @"C:\SomeDir\states.dat";
 
        try
        {
            // создаем объект BinaryWriter
            using (BinaryWriter writer = new BinaryWriter(File.Open(path, FileMode.OpenOrCreate)))
            {
                // записываем в файл значение каждого поля структуры
                foreach (State s in states)
                {
                    writer.Write(s.name);
                    writer.Write(s.capital);
                    writer.Write(s.area);
                    writer.Write(s.people);
                }
            }
            // создаем объект BinaryReader
            using (BinaryReader reader = new BinaryReader(File.Open(path, FileMode.Open)))
            {
                // пока не достигнут конец файла
                // считываем каждое значение из файла
                while (reader.PeekChar() > -1)
                {
                    string name = reader.ReadString();
                    string capital = reader.ReadString();
                    int area = reader.ReadInt32();
                    double population = reader.ReadDouble();
 
                    Console.WriteLine("Страна: {0}  столица: {1}  площадь {2} кв. км   численность населения: {3} млн. чел.", 
                        name, capital, area, population);
                }
            }
        }
        catch (Exception e)
        {
            Console.WriteLine(e.Message);
        }
        Console.ReadLine();
    }
}
```

Итак, у нас есть структура **State** с некоторым набором полей. В основной программе создаем массив структур и записываем с помощью **BinaryWriter**. Этот класс в качестве параметра в конструкторе принимает объект **Stream**, который создается вызовом `File.Open(path, FileMode.OpenOrCreate)`.

Затем в цикле пробегаемся по массиву структур и записываем каждое поле структуры в поток. В том порядке, в каком эти значения полей записываются, в том порядке они и будут размещаться в файле.

Затем считываем из записанного файла. Конструктор класса **BinaryReader** также в качестве параметра принимает объект потока, только в данном случае устанавливаем в качестве режима _FileMode.Open_: `new BinaryReader(File.Open(path, FileMode.Open))`

В цикле **while** считываем данные. Чтобы узнать окончание потока, вызываем метод *PeekChar*. Этот метод считывает следующий символ и возвращает его числовое представление. Если символ отсутствует, то метод возвращает `-1`, что будет означать, что мы достигли конца файла.

В цикле последовательно считываем значения поле структур в том же порядке, в каком они записывались.

Таким образом, классы **BinaryWriter** и **BinaryReader** очень удобны для работы с бинарными файлами, особенно когда нам известна структура этих файлов. В то же время для хранения и считывания более комплексных объектов, например, объектов классов, лучше подходит другое решение - сериализация.

## Бинарная сериализация. **BinaryFormatter**

В прошлых темах было рассмотрено как сохранять и считывать информацию с текстовых и бинарных файлов с помощью классов из пространства `System.IO`. Но .NET также предоставляет еще один механизм для удобной работы с бинарными файлами и их данными - бинарную **сериализацию**. **Сериализация** представляет процесс преобразования какого-либо объекта в поток байтов. После преобразования мы можем этот поток байтов или записать на диск или сохранить его временно в памяти. А при необходимости можно выполнить обратный процесс - **десериализацию**, то есть получить из потока байтов ранее сохраненный объект.

### Атрибут **Serializable**

Чтобы объект определенного класса можно было сериализовать, надо этот класс пометить атрибутом **Serializable**:

```cs
[Serializable]
class Person
{
    public string Name { get; set; }
    public int Year { get; set; }
 
    public Person(string name, int year)
    {
        Name = name;
        Year = year;
    }
}
```

При отстутствии данного атрибута объект **Person** не сможет быть сериализован, и при попытке сериализации будет выброшено исключение **SerializationException**.

Сериализация применяется к свойствам и полям класса. Если мы не хотим, чтобы какое-то поле класса сериализовалось, то мы его помечаем атрибутом **NonSerialized**:

```cs
[Serializable]
class Person
{
    public string Name { get; set; }
    public int Year { get; set; }
     
    [NonSerialized]
    public string accNumber;
     
    public Person(string name, int year, string acc)
    {
        Name = name;
        Year = year;
        accNumber = acc;
    }
}
```

При наследовании подобного класса, следует учитывать, что атрибут **Serializable** автоматически не наследуется. И если мы хотим, чтобы производный класс также мог бы быть сериализован, то опять же мы применяем к нему атрибут:

```cs
[Serializable]
class Worker : Person
```

Для бинарной сериализации применяется класс **BinaryFormatter**:

```cs
using System;
using System.IO;
using System.Runtime.Serialization.Formatters.Binary;
 
namespace Serialization
{
    [Serializable]
    class Person
    {
        public string Name { get; set; }
        public int Age { get; set; }
 
        public Person(string name, int age)
        {
            Name = name;
            Age = age;
        }
    }
     
    class Program
    {
        static void Main(string[] args)
        {
            // объект для сериализации
            Person person = new Person("Tom", 29);
            Console.WriteLine("Объект создан");
 
            // создаем объект BinaryFormatter
            BinaryFormatter formatter = new BinaryFormatter();
            // получаем поток, куда будем записывать сериализованный объект
            using (FileStream fs = new FileStream("people.dat", FileMode.OpenOrCreate))
            {
                formatter.Serialize(fs, person);
 
                Console.WriteLine("Объект сериализован");
            }
 
            // десериализация из файла people.dat
            using (FileStream fs = new FileStream("people.dat", FileMode.OpenOrCreate))
            {
                Person newPerson = (Person)formatter.Deserialize(fs);
 
                Console.WriteLine("Объект десериализован");
                Console.WriteLine($"Имя: {newPerson.Name} --- Возраст: {newPerson.Age}");
            }
 
            Console.ReadLine();
        }
    }
}
```

Так как класс **BinaryFormatter** определен в пространстве имен `System.Runtime.Serialization.Formatters.Binary`, то в самом начале подключаем его.

У нас есть простенький класс **Person**, который объявлен с атрибутом **Serializable**. Благодаря этому его объекты будут доступны для сериализации.

Далее создаем объект *BinaryFormatter*: `BinaryFormatter formatter = new BinaryFormatter();`

Затем последовательно выполняем сериализацию и десериализацию. Для обоих операций нам нужен поток, в который либо сохранять, либо из которого считывать данные. Данный поток представляет объект **FileStream**, который записывает нужный нам объект **Person** в файл `people.dat`.

Сериализация одним методом `formatter.Serialize(fs, person)` добавляет все данные об объекте **Person** в файл `people.dat`.

При десериализации нам нужно еще преобразовать объект, возвращаемый функцией *Deserialize*, к типу **Person**: `(Person)formatter.Deserialize(fs)`.

Как вы видите, **сериализация** значительно упрощает процесс сохранения объектов в бинарную форму по сравнению, например, с использованием связки классов **BinaryWriter**/**BinaryReader**.

Хотя мы взяли лишь один объект **Person**, но равным образом мы можем использовать и массив подобных объектов, список или иную коллекцию, к которой применяется атрибут **Serializable**. Посмотрим на примере массива:

```cs
Person person1 = new Person("Tom", 29);
Person person2 = new Person("Bill", 25);
// массив для сериализации
Person[] people = new Person[] { person1, person2 };
 
BinaryFormatter formatter = new BinaryFormatter();
 
using (FileStream fs = new FileStream("people.dat", FileMode.OpenOrCreate))
{
    // сериализуем весь массив people
    formatter.Serialize(fs, people);
 
    Console.WriteLine("Объект сериализован");
}
 
// десериализация
using (FileStream fs = new FileStream("people.dat", FileMode.OpenOrCreate))
{
    Person[] deserilizePeople = (Person[])formatter.Deserialize(fs);
 
    foreach (Person p in deserilizePeople)
    {
        Console.WriteLine($"Имя: {p.Name} --- Возраст: {p.Age}");
    }
}
```

Предыдущая лекция | &nbsp; | Следующая лекция
:----------------:|:----------:|:----------------:
[Исключения. Null.](./t5_exception.md) | [Содержание](../readme.md#тема-5-продвинутый-c-функции-лямбды-исключения-работа-с-файлами-многопоточность-регулярные-выражения) | [Многопоточность. Потоки, асинхронные вычисления](./t5_thread_async.md)
