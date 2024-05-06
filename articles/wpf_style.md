Предыдущая лекция | &nbsp; | Следующая лекция
:----------------:|:----------:|:----------------:
[Вывод данных согласно макета (ListBox, Image)](./articles/wpf_listbox.md) | [Содержание](../readme.md#тема-8-оконные-приложения) | [Создание окон. Модальные окна](./wpf_window.md)

>Два инициативных студента по итогам прошлой лекции решили сделать переключение вида отображения "список" и "плитка" кнопкой. Нарыли интересную тему про стили...

# [Стили и темы](https://metanit.com/sharp/wpf/10.php)

## Стили

Стили позволяют определить набор некоторых свойств и их значений, которые потом могут применяться к элементам в `xaml`. Стили хранятся в ресурсах и отделяют значения свойств элементов от пользовательского интерфейса. Также стили могут задавать некоторые аспекты поведения элементов с помощью триггеров. Аналогом стилей могут служить каскадные таблицы стилей (CSS), которые применяются в коде html на веб-страницах.

Зачем нужны стили? Стили помогают создать стилевое единообразие для определенных элементов. Допустим, у нас есть следующий код xaml:

```xml
<StackPanel 
    x:Name="buttonsStack" 
    Background="Black" 
>
    <Button 
        x:Name="button1" 
        Margin="10" 
        Content="Кнопка 1" 
        FontFamily="Verdana" 
        Foreground="White" 
        Background="Black" />
    <Button 
        x:Name="button2" 
        Margin="10" 
        Content="Кнопка 2" 
        FontFamily="Verdana" 
        Foreground="White" 
        Background="Black"/>
</StackPanel>
```

Здесь обе кнопки применяют ряд свойств с одними и теми же значениями. Однако в данном случае мы вынуждены повторяться. Частично, проблему могло бы решить использование ресурсов:

```xml
<Window 
    ...
>
    <Window.Resources>
        <FontFamily 
            x:Key="buttonFont">
            Verdana
        </FontFamily>
        <SolidColorBrush 
            Color="White" 
            x:Key="buttonFontColor" />
        <SolidColorBrush 
            Color="Black" 
            x:Key="buttonBackColor" />
        <Thickness 
            x:Key="buttonMargin" 
            Bottom="10" 
            Left="10" 
            Top="10" 
            Right="10" />
    </Window.Resources>

    <StackPanel 
        x:Name="buttonsStack" 
        Background="Black" >
        <Button 
            x:Name="button1" 
            Content="Кнопка 1"
            Margin="{StaticResource buttonMargin}"
            FontFamily="{StaticResource buttonFont}"
            Foreground="{StaticResource buttonFontColor}"
            Background="{StaticResource buttonBackColor}" />
        <Button 
            x:Name="button2" 
            Content="Кнопка 2"
            Margin="{StaticResource buttonMargin}"
            FontFamily="{StaticResource buttonFont}"
            Foreground="{StaticResource buttonFontColor}"
            Background="{StaticResource buttonBackColor}"/>
    </StackPanel>
</Window>
```

Однако в реальности код раздувается, опть же приходится писать много повторяющейся информации. И в этом плане стили предлагают более элегантное решение:

```xml
<Window 
    ...
>
    <Window.Resources>
        <Style x:Key="BlackAndWhite">
            <Setter 
                Property="Control.FontFamily" 
                Value="Verdana" />
            <Setter 
                Property="Control.Background" 
                Value="Black" />
            <Setter 
                Property="Control.Foreground" 
                Value="White" />
            <Setter 
                Property="Control.Margin" 
                Value="10" />
        </Style>
    </Window.Resources>

    <StackPanel 
        x:Name="buttonsStack" 
        Background="Black" >
        <Button 
            x:Name="button1" 
            Content="Кнопка 1"
            Style="{StaticResource BlackAndWhite}" />
        <Button 
            x:Name="button2" 
            Content="Кнопка 2"
            Style="{StaticResource BlackAndWhite}"/>
    </StackPanel>
</Window>
```

Результат будет тот же, однако теперь мы избегаем ненужного повторения. Более того теперь мы можем управлять всеми нужными нам свойствами как единым целым - одним стилем.

Стиль создается как ресурс с помощью объекта **Style**, который представляет класс **System.Windows.Style**. И как любой другой ресурс, он обязательно должен иметь ключ. С помощью коллекции **Setters** определяется группа свойств, входящих в стиль. В нее входят объекты **Setter**, которые имеют следующие свойства:

* **Property**: указывает на свойство, к которому будет применяться данный сеттер. Имеет следующий синтаксис: `Property="Тип_элемента.Свойство_элемента"`. Выше в качестве типа элемента использовался **Control**, как общий для всех элементов. Поэтому данный стиль мы могли бы применить и к **Button**, и к **TextBlock**, и к другим элементам. Однако мы можем и конкретизировать элемент, например, **Button**:

    ```xml
    <Setter 
        Property="Button.FontFamily" 
        Value="Arial" />
    ```

* **Value**: устанавливает значение

Если значение свойства представляет сложный объект, то мы можем его вынести в отдельный элемент:

```xml
<Style 
    x:Key="BlackAndWhite">
    <Setter 
        Property="Control.Background">
        <Setter.Value>
            <LinearGradientBrush>
                <LinearGradientBrush.GradientStops>
                    <GradientStop 
                        Color="White" 
                        Offset="0" />
                    <GradientStop 
                        Color="Black" 
                        Offset="1" />
                </LinearGradientBrush.GradientStops>
            </LinearGradientBrush>
        </Setter.Value>
    </Setter>
    <Setter 
        Property="Control.FontFamily" 
        Value="Verdana" />
    <Setter 
        Property="Control.Foreground" 
        Value="White" />
    <Setter 
        Property="Control.Margin" 
        Value="10" />
</Style>
```

### TargetType

Hам необязательно прописывать для всех кнопок стиль. Мы можем в самом определении стиля с помощью свойства _TargetType_ задать тип элементов. В этом случае стиль будет автоматически применяться ко всем кнопкам в окне:

```xml
<Window ...>
    <Window.Resources>
        <Style 
            TargetType="Button">
            <Setter 
                Property="FontFamily" 
                Value="Verdana" />
            <Setter 
                Property="Background" 
                Value="Black" />
            <Setter 
                Property="Foreground" 
                Value="White" />
            <Setter 
                Property="Margin" 
                Value="10" />
        </Style>
    </Window.Resources>

    <StackPanel 
        x:Name="buttonsStack" 
        Background="Black" >
        <Button 
            x:Name="button1" 
            Content="Кнопка 1"  />
        <Button 
            x:Name="button2" 
            Content="Кнопка 2" />
    </StackPanel>
</Window>
```

Причем в этом случае нам уже не надо указывать у стиля ключ `x:Key` несмотря на то, что это ресурс.

Также если используем свойство _TargetType_, то в значении атрибута _Property_ уже необязательно указывать тип, то есть `Property="Control.FontFamily"`. И в данном случае тип можно просто опустить: `Property="FontFamily"`

Если же необходимо, чтобы к какой-то кнопке не применялся автоматический стиль, то ее стилю присваивают значение null

```xml
<Button 
    x:Name="button2" 
    Content="Кнопка 2" 
    Style="{x:Null}" />
```

### Определение обработчиков событий с помощью стилей

Кроме коллекции **Setters** стиль может определить другую коллекцию - **EventSetters**, которая содержит объекты **EventSetter**. Эти объекты позволяют связать события элементов с обработчиками. Например, подключим все кнопки к одному обработчику события **Click**:

```xml
<Style 
    TargetType="Button">
    ...
    <EventSetter 
        Event="Button.Click" 
        Handler="Button_Click" />
</Style>
```

Соответственно в файле кода `c#` у нас должен быть определен обработчик **Button_Click**:

```cs
private void Button_Click(object sender, RoutedEventArgs e)
{
    Button clickedButton = (Button)sender;
    MessageBox.Show(clickedButton.Content.ToString());
}
```

### Наследование стилей и свойство _BasedOn_

У класса **Style** еще есть свойство _BasedOn_, с помощью которого можно наследовать и расширять существующие стили:

```xml
<Window.Resources>
    <Style x:Key="ButtonParentStyle">
        <Setter Property="Button.FontFamily" Value="Andy" />
    </Style>
    <Style 
        x:Key="ButtonChildStyle" 
        BasedOn="{StaticResource ButtonParentStyle}">
        <Setter 
            Property="Button.BorderBrush" 
            Value="Red" />
        <Setter 
            Property="Button.FontFamily" 
            Value="Verdana" />
    </Style>
</Window.Resources>
```

Cвойство _BasedOn_ в качестве значения принимает существующий стиль, определяя его как статический ресурс. В итоге он объединяет весь функционал родительского стиля со своим собственным.

Если в дочернем стиле есть сеттеры для свойств, которые также используются в родительском стиле, как в данном случае сеттер для свойства _Button.FontFamily_, то дочерний стиль переопределяет родительский стиль.

### Стили в C#

В `C#` стили представляют объект **System.Windows.Style**. Используя его, мы можем добавлять сеттеры и устанавливать стиль для нужных элементов:


```cs
public MainWindow()
{
    InitializeComponent();

    Style buttonStyle = new Style();
    buttonStyle.Setters.Add(
        new Setter { 
            Property = Control.FontFamilyProperty, 
            Value = new FontFamily("Verdana") });
    buttonStyle.Setters.Add(
        new Setter { 
            Property = Control.MarginProperty, 
            Value = new Thickness(10) });
    buttonStyle.Setters.Add(
        new Setter { 
            Property = Control.BackgroundProperty, 
            Value = new SolidColorBrush(Colors.Black) });
    buttonStyle.Setters.Add(
        new Setter { 
            Property = Control.ForegroundProperty, 
            Value = new SolidColorBrush(Colors.White) });
    buttonStyle.Setters.Add(
        new EventSetter { 
            Event= Button.ClickEvent, 
            Handler= new RoutedEventHandler( Button_Click) });

    button1.Style = buttonStyle;
    button2.Style = buttonStyle;
}
```

При создании сеттера нам надо использовать свойство зависимостей, например, `Property = Control.FontFamilyProperty`. Причем для свойства _Value_ у сеттера должен быть установлен объект именно того типа, которое хранится в этом свойстве зависимости. Так, свойство зависимости _MarginProperty_ хранит объект типа **Thickness**, поэтому определение сеттера выглядит следующим образом:

```cs
new Setter { 
    Property = Control.MarginProperty, 
    Value = new Thickness(10) }
```

## Темы

Стили позволяют задать стилевые особенности для определенного элемента или элементов одного типа. Но иногда возникает необходимость применить ко всем элементам какое-то общее стилевое единообразие. И в этом случае мы можем объединять стили элементов в темы. Например, все элементы могут выполнены в светлом стиле, или, наоборот, к ним может применяться так называемая "ночная тема". Более того может возникнуть необходимость не просто определить общую тему для всех элементов, но и иметь возможность динамически выбирать понравившуюся тему из списка тем. И в данной статье рассмотрим, как это сделать.

Пусть у нас есть окно приложения с некоторым набором элементов:

```xml
<Window 
    ...
    Style="{DynamicResource WindowStyle}"
>
    <StackPanel>
        <ComboBox 
            x:Name="styleBox" />
        <Button 
            Content="Hello WPF" 
            Style="{DynamicResource ButtonStyle}" />
        <TextBlock 
            Text="Windows Presentation Foundation" 
            Style="{DynamicResource TextBlockStyle}" />
    </StackPanel>
</Window>
```

Для примера здесь определены кнопка, текстовый блок и выпадающий список, в котором позже будут выбираться темы.

К элементам окна уже применяются некоторые стили. Причем следует отметить, что стили указывают на динамические (не статические) ресурсы. Однако сами эти ресурсы еще не заданы. Поэтому зададим их.

Для этого добавим в проект новый файл словаря ресурсов, который назовем `light.xaml`, и определим в нем некоторый набор ресурсов:

```xml
<ResourceDictionary 
    xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
    xmlns:local="clr-namespace:ThemesApp">
    <Style 
        x:Key="TextBlockStyle" 
        TargetType="TextBlock">
        <Setter 
            Property="Background" 
            Value="White" />
        <Setter 
            Property="Foreground" 
            Value="Gray" />
    </Style>
    <Style 
        x:Key="WindowStyle" 
        TargetType="Window">
        <Setter 
            Property="Background" 
            Value="White" />
    </Style>
    <Style 
        x:Key="ButtonStyle" 
        TargetType="Button">
        <Setter 
            Property="Background" 
            Value="White" />
        <Setter 
            Property="Foreground" 
            Value="Gray" />
        <Setter 
            Property="BorderBrush" 
            Value="Gray" />
    </Style>
</ResourceDictionary>
```

Здесь указаны все те стили, которые применяются элементами окна.

Но теперь также добавим еще один словарь ресурсов, который назовем `dark.xaml` и в котором определим следующий набор ресурсов:

```xml
<ResourceDictionary 
    xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
    xmlns:local="clr-namespace:ThemesApp">
    <Style 
        x:Key="TextBlockStyle" 
        TargetType="TextBlock">
        <Setter 
            Property="Background" 
            Value="Gray" />
        <Setter 
            Property="Foreground" 
            Value="White" />
    </Style>
    <Style 
        x:Key="WindowStyle" 
        TargetType="Window">
        <Setter 
            Property="Background" 
            Value="Gray" />
    </Style>
    <Style 
        x:Key="ButtonStyle" 
        TargetType="Button">
        <Setter 
            Property="Background" 
            Value="Gray" />
        <Setter 
            Property="Foreground" 
            Value="White" />
        <Setter 
            Property="BorderBrush" 
            Value="White" />
    </Style>
</ResourceDictionary>
```

Здесь определены те же самые стили, только их значения уже отличаются. То есть фактически мы создали две темы: для светлого и темного стилей.

Теперь применим эти стили. Для этого изменим файл `MainWindow.xaml.cs` следующим образом:


```cs
public partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();

        List<string> styles = new List<string> { "light", "dark" };
        styleBox.SelectionChanged += ThemeChange;
        styleBox.ItemsSource = styles;
        styleBox.SelectedItem = "dark";
    }

    private void ThemeChange(object sender, SelectionChangedEventArgs e)
    {
        string style = styleBox.SelectedItem as string;
        // определяем путь к файлу ресурсов
        var uri = new Uri(style + ".xaml", UriKind.Relative);
        // загружаем словарь ресурсов
        ResourceDictionary resourceDict = 
            Application.LoadComponent(uri) as ResourceDictionary;
        // очищаем коллекцию ресурсов приложения
        Application.Current.Resources.Clear();
        // добавляем загруженный словарь ресурсов
        Application.Current.Resources.MergedDictionaries.Add(resourceDict);
    }
}
```

К элементу **ComboBox** цепляется обработчик _ThemeChange_, который срабатывает при выборе элемента в списке.

В методе **ThemeChange** получаем выделенный элемент, который представляет название темы. По нему загружаем локальный словарь ресурсов и добавляем этот словарь в коллекцию ресурсов приложения.

В итоге при выборе элемента в списке будет меняться применяемая к приложению тема.

## Переключение вида списка

1. Переносим настройки **ListBox** в ресурсы окна (в том числе и шаблон элемента списка):

    ```xml
    <Window.Resources>
        <Style 
            x:Key="StackStyle" 
            TargetType="ListBox"
        >
            <Setter 
                Property="ItemsPanel"
            >
                <Setter.Value>
                    <ItemsPanelTemplate>
                        <StackPanel 
                            Orientation="Vertical"/>
                    </ItemsPanelTemplate>
                </Setter.Value>
            </Setter>

            <Setter 
                Property="ItemTemplate"
            >
                <Setter.Value>
                    <DataTemplate>
                        <Border 
                            BorderThickness="2" 
                            BorderBrush="DarkRed" 
                            CornerRadius="4" 
                            Margin="4"
                        >
                            <Grid>
                                <Grid.ColumnDefinitions>
                                    <ColumnDefinition Width="64"/>
                                    <ColumnDefinition Width="*"/>
                                    <ColumnDefinition Width="auto"/>
                                </Grid.ColumnDefinitions>
                                
                                <Image 
                                    Width="64" 
                                    Height="64" 
                                    Source="{Binding ImageBitmap}"/>
                                
                                <StackPanel 
                                    Grid.Column="1"  
                                    Orientation="Vertical" 
                                    Margin="5,2,0,5"
                                >
                                    <TextBlock Text="{Binding name}"/>
                                    <TextBlock Text="{Binding surname}"/>
                                </StackPanel>

                                <TextBlock 
                                    Grid.Column="2"  
                                    Text="{Binding age}" 
                                    Margin="0,2,10,0"/>
                            </Grid>
                        </Border>
                    </DataTemplate>
                </Setter.Value>
            </Setter>
        </Style>
        <Style 
            x:Key="WrapStyle" 
            TargetType="ListBox"
        >
            <Setter 
                Property="ItemsPanel"
            >
                <Setter.Value>
                    <ItemsPanelTemplate>
                        <WrapPanel 
                            HorizontalAlignment="Center"
                            ItemWidth="200"/>
                    </ItemsPanelTemplate>
                </Setter.Value>
            </Setter>

            <Setter 
                Property="ItemTemplate"
            >
                <Setter.Value>
                    <DataTemplate>
                        <Border 
                            BorderThickness="1" 
                            BorderBrush="Black" 
                            CornerRadius="5" 
                            Margin="5"
                        >
                            <StackPanel 
                                Orientation="Vertical"
                            >
                                <Image 
                                    Width="200" 
                                    Source="{Binding ImageBitmap}"/>
                                <TextBlock 
                                    Text="{Binding name}"
                                    HorizontalAlignment="Center"/>
                                <TextBlock 
                                    Text="{Binding surname}"
                                    HorizontalAlignment="Center"/>
                                <TextBlock 
                                    Text="{Binding age}"
                                    HorizontalAlignment="Center"/>
                            </StackPanel>
                        </Border>
                    </DataTemplate>
                </Setter.Value>
            </Setter>
        </Style>
    </Window.Resources>
    ```

2. **ListBox**-у задаем стиль по-умолчанию

    ```xml
    <ListBox
        x:Name="catListBox"
        Style="{StaticResource StackStyle}"
        ...
    ```

    Убираем настройки для `<ListBox.ItemsPanel>` и `<ListBox.ItemTemplate>`, а для `<ListBox.ItemContainerStyle>` возвращаем (хотя он нужен только для стека и его тоже можно перенести в соответствующий стиль):

    ```xml
    <ListBox.ItemContainerStyle>
        <Style 
            TargetType="ListBoxItem">
            <Setter 
                Property="HorizontalContentAlignment"
                Value="Stretch" />
        </Style>
    </ListBox.ItemContainerStyle>
    ```

3. В верхнюю панель (где у нас элементы управления для фильтраци, поиска и т.п.) добавляем кнопку "Сменить стиль" и в её обработчике переопределяем стиль для **ListBox**-а

    ```cs
    // храним текущий стиль
    private string currentStyle = "StackStyle";

    private void ToggleView_Click(object sender, RoutedEventArgs e)
    {
        currentStyle = currentStyle == "StackStyle" ? "WrapStyle" : "StackStyle";
        var newStyle = (Style)TryFindResource(currentStyle)
        if (newStyle != null)
            catListBox.Style = newStyle;
    }
    ```

---

## Задание на дом

Реализовать все примеры из лекции. В репозиторий добавить скриншоты результатов работы.

Предыдущая лекция | &nbsp; | Следующая лекция
:----------------:|:----------:|:----------------:
[Вывод данных согласно макета (ListBox, Image)](./articles/wpf_listbox.md) | [Содержание](../readme.md#тема-8-оконные-приложения) | [Создание окон. Модальные окна](./wpf_window.md)
