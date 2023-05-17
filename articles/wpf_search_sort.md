[Фильтрация данных](./wpf_filtering.md) | [Содержание](../readme.md#тема-8-оконные-приложения)

# Поиск, сортировка

В этой теме мы познакомимся еще с двумя визуальными элементами: **TextBox** (ввод строки для поиска) и **RadioButton** (сортировка по одному полю)

## Поиск

1. В разметке окна (в элемент WrapPanel) добавляем элемент для ввода теста - TextBox

    ```xml
    <Label 
        Content="искать" 
        VerticalAlignment="Center"/>
    <TextBox
        Width="200"
        VerticalAlignment="Center"
        x:Name="SearchFilterTextBox" 
        KeyUp="SearchFilter_KeyUp"/>
    ```    

1. В коде окна создаем переменную для хранения строки поиска и запоминаем её в обработчике ввода текста (SearchFilter_KeyUp)

    ```cs
    private string searchFilter = ""; 

    private void SearchFilter_KeyUp(object sender, KeyEventArgs e)
    {
        searchFilter = SearchFilterTextBox.Text;
        Invalidate();
    }
    ```

1. Дорабатываем геттер списка кошек, чтобы после фильтра по возрасту срабатывал ещё и фильтр по кличке

    ```cs
    get
    {
        // сохраняем во временную переменную полный список
        var res = _catList;

        // фильтруем по возрасту
        res = res.Where(c=>(c.Age>=selectedAge.ageFrom && c.Age<selectedAge.ageTo));

        // если фильтр не пустой, то ищем ВХОЖДЕНИЕ подстроки поиска в кличке без учета регистра
        if(SearchFilter != "")
            res = res.Where(c => c.Name.IndexOf(
                searchFilter, 
                StringComparison.OrdinalIgnoreCase) >= 0);

        return res;
    }
    ```

## Сортировка

>Мы, в рамках знакомства с визуальными элементами, будем использовать радио-кнопки, но, если вариантов сортировки более одного, то лучше использовать тот-же выпадающий список

Мы будем сортировать по возрасту

Выбранный вариант будем определять по атрибуту **Tag**. Этот атрибут есть у всех элементов и его тип **объект**. 

1. В разметке добавляем радиокнопки

    ```xml
    <Label 
        Content="Возраст:" 
        VerticalAlignment="Center"/>
    <RadioButton
        GroupName="Age"
        Tag="1"
        Content="по возрастанию"
        IsChecked="True"
        Checked="RadioButton_Checked"
        VerticalAlignment="Center"/>
    <RadioButton
        GroupName="Age"
        Tag="2"
        Content="по убыванию"
        Checked="RadioButton_Checked"
        VerticalAlignment="Center"/>
    ```

    У группы радио-кнопок одновременно может быть выбран только один вариант. Группа задается атрибутом **GroupName** 

1. В коде добавляем переменную для хранения варианта сортировки и обработчик смены варианта сортировки

    >Мы в атрибуте **Tag** храним просто уникальное значение, но при необходимости можем *прибиндить* какой-нибудь объект и в обработчике получить его: `(sender as RadioButton).Tag as SomeClass`.

    ```cs
    private bool sortAsc = true;

    private void RadioButton_Checked(object sender, RoutedEventArgs e)
    {
        sortAsc = (sender as RadioButton).Tag.ToString() == "1";
        Invalidate();
    }
    ```

1. И дорабатываем геттер списка кошек

    ```cs
    ...
    if (sortAsc) res = res.OrderBy(c=>c.Age);
    else res = res.OrderByDescending(c => c.Age);

    return res;
    ```

[Фильтрация данных](./wpf_filtering.md) | [Содержание](../readme.md#тема-8-оконные-приложения)
