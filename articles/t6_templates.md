<table style="width: 100%;"><tr><td style="width: 40%;">
<a href="../articles/t6_linq.md">LINQ
</a></td><td style="width: 20%;">
<a href="../readme.md">Содержание
</a></td><td style="width: 40%;">
<a href="../articles/t7_dll.md">Библиотеки классов
</a></td><tr></table>

# Шаблоны проектирования (порождающие)

>содрано [отсюда](https://tproger.ru/translations/design-patterns-simple-words-1/) с переводом на C# и проверкой

**Шаблоны проектирования** — это руководства по решению повторяющихся проблем. Это не классы, пакеты или библиотеки, которые можно было бы подключить к вашему приложению и сидеть в ожидании чуда. Они скорее являются методиками, как решать определенные проблемы в определенных ситуациях.

Википедия описывает их следующим образом:

Шаблон проектирования, или паттерн, в разработке программного обеспечения — повторяемая архитектурная конструкция, представляющая собой решение проблемы проектирования, в рамках некоторого часто возникающего контекста.

## Будьте осторожны

* шаблоны проектирования не являются решением всех ваших проблем;
* не пытайтесь использовать их в обязательном порядке — это может привести к негативным последствиям. Шаблоны — это подходы к решению проблем, а не решения для поиска проблем;
* если их правильно использовать в нужных местах, то они могут стать спасением, а иначе могут привести к ужасному беспорядку.

## Типы шаблонов

Шаблоны бывают следующих трех видов:

* Порождающие
* Структурные
* Поведенческие

## Порождающие шаблоны

Этот тип особенно важен, когда система зависит не столько от наследования классов, сколько от [композиции](https://habr.com/ru/post/325478/) (композиция — это когда один объект предоставляет другому свою функциональность частично или полностью). Порождающие паттерны отвечают за создание объектов и позволяют системе быть независимой от типов этих самых объектов и от процесса порождения.

В свою очередь, порождающие паттерны делятся на:

* Singleton
* Simple Factory
* Factory Method
* Abstract Factory
* Builder
* Prototype

### Одиночка (Singleton)

**Одиночка** — порождающий шаблон проектирования, гарантирующий, что в однопроцессном приложении будет единственный экземпляр некоторого класса, и предоставляющий глобальную точку доступа к этому экземпляру.

**Пример из жизни**: В семье всего одна пара тапочек, одеть их может только один человек.

**Простыми словами**: Обеспечивает тот факт, что создаваемый объект является единственным объектом своего класса.

В C# он реализуется статическими свойствами класса (из темы про классы мы помним, что статические переменные определяются при первом обращении):

```cs
class Core
{
    public static SomeEntities DB = new SomeEntities();
}
```

### Шаблон Simple Factory (Простая Фабрика)

В объектно-ориентированном программировании (ООП), фабрика — это объект для создания других объектов. Формально фабрика — это функция или метод, который возвращает объекты изменяющегося прототипа или класса из некоторого вызова метода, который считается «новым».

**Пример из жизни**: Представьте, что вам надо построить дом, и вам нужны двери. Было бы глупо каждый раз, когда вам нужны двери, надевать вашу столярную форму и начинать делать дверь. Вместо этого вы заказываете её на фабрике.

**Простыми словами**: Простая фабрика генерирует экземпляр для клиента, не раскрывая никакой логики.

Шаблон предназначен для инкапсуляции процесса образования объектов с помощью отдельного класса. «Простая Фабрика» удобна, но за простоту приходится платить: привязка к конкретной реализации исключает гибкость системы. *Simple Factory* следует использовать только там, где архитектура не будет изменяться.

Допустим, у нас есть интерфейс двери и класс, реализующий деревянную дверь:

```cs
interface IDoor
{
    double GetWidth();
    double GetHeight();
}

class WoodenDoor : IDoor 
{
    private double Width { get; set; }
    private double Height { get; set; }

    public WoodenDoor(double width, double height) {
        Width = width;
        Height = height;
    }

    public double GetWidth()
    {
        return Width;
    }

    public double GetHeight()
    {
        return Height;
    }
}
```

Далее появляется завод, который изготавливает дверь и возвращает её нам:

```cs
class DoorFactory 
{ 
    static public IDoor MakeDoor(double Width, double Height) {
        return new WoodenDoor(Width, Height);
    }
}
```

И после этого мы можем сделать дверь на фабрике:

```cs
var door = DoorFactory.MakeDoor(100, 200);
```

Как видно из кода, вызвав статический метод `DoorFactory.MakeDoor(100, 200)` мы получили не экземпляр завода, а экземпляр двери.

**Когда использовать**: Когда создание объекта — это не просто несколько присвоений, а какая-то логика, тогда имеет смысл создать отдельную фабрику вместо повторения одного и того же кода повсюду.

### Шаблон Fabric Method (Фабричный метод)

**Фабричный метод** — порождающий шаблон проектирования, предоставляющий подклассам интерфейс для создания экземпляров некоторого класса. В момент создания наследники могут определить, какой класс создавать. Иными словами, данный шаблон делегирует создание объектов наследникам родительского класса. Это позволяет использовать в коде программы не специфические классы, а манипулировать абстрактными объектами на более высоком уровне.

**Пример из жизни**: Рассмотрим пример с менеджером по найму. Невозможно одному человеку провести собеседования со всеми кандидатами на все вакансии. В зависимости от вакансии он должен распределить этапы собеседования между разными людьми.

**Простыми словами**: Менеджер предоставляет способ делегирования логики создания экземпляра дочерним классам.

Изначально у нас есть интерфейс Interviewer и несколько реализаций для него:

```kt
interface Interviewer {
    fun askQuestions()
}

class Developer : Interviewer {
    override fun askQuestions() = println("Спрашивает про шаблоны проектирования!")
}

class CommunityExecutive : Interviewer {
    override fun askQuestions() = println("Спрашивает о работе с сообществом")
}
```

Теперь создаем менеджера по подбору персонала:

```kt
abstract class HiringManager {
    lateinit var interviewer: Interviewer

    // Фабричный метод
    abstract fun makeInterviewer(): Interviewer

    fun takeInterview() {
        interviewer = makeInterviewer()
        interviewer.askQuestions()
    }
}
```

И теперь любой дочерний класс может расширять его и предоставлять необходимого интервьюера:

```kt
class DevelopmentManager : HiringManager() {
    override fun makeInterviewer(): Interviewer {
        return Developer()
    }
}

class MarketingManager : HiringManager() {
    override fun makeInterviewer(): Interviewer {
        return CommunityExecutive()
    }
}
```

После чего можно использовать:

```kt
fun main() {
    var devManager = DevelopmentManager()
    devManager.takeInterview() // Вывод: Спрашивает о шаблонах проектирования!

    var marketingManager = MarketingManager()
    marketingManager.takeInterview() // Вывод: Спрашивает о работе с сообществом
}
```

**Когда использовать**: Полезен, когда есть некоторая общая обработка в классе, но необходимый подкласс динамически определяется во время выполнения. Иными словами, когда клиент не знает, какой именно подкласс ему может понадобиться.

### Абстрактная фабрика (Abstract Factory)

**Абстрактная фабрика** — порождающий шаблон проектирования, предоставляет интерфейс для создания семейств взаимосвязанных или взаимозависимых объектов, не специфицируя их конкретных классов. Шаблон реализуется созданием абстрактного класса Factory, который представляет собой интерфейс для создания компонентов системы (например, для оконного интерфейса он может создавать окна и кнопки). Затем пишутся классы, реализующие этот интерфейс.

**Пример из жизни**: Расширим наш пример про двери из простой фабрики. В зависимости от ваших нужд вам понадобится деревянная дверь из одного магазина, железная дверь — из другого или пластиковая — из третьего. Кроме того, вам понадобится соответствующий специалист: столяр для деревянной двери, сварщик для железной двери и так далее. Как вы можете заметить, тут есть зависимость между дверьми.

**Простыми словами**: Фабрика фабрик. Фабрика, которая группирует индивидуальные, но связанные/зависимые фабрики без указания их конкретных классов.

Обратимся к коду. Используем пример про двери. Сначала у нас есть интерфейс Door и несколько его реализаций:

```kt
interface Door {
    fun getDescription()
}

class WoodenDoor : Door {
    override fun getDescription() = println("Я деревянная дверь")
}

class IronDoor : Door {
    override fun getDescription() = println("Я железная дверь")
}
```

Затем у нас есть несколько мастеров по установке для каждого типа дверей:

```kt
interface DoorFittingExpert {
    fun getDescription()
}

class Welder : DoorFittingExpert {
    override fun getDescription() = println("Я слесарь, работаю только с железными дверьми")
}

class Carpenter : DoorFittingExpert {
    override fun getDescription() = println("Я столяр, работаю только с деревянными дверьми")
}
```

Теперь нам нужна фабрика дверей, которая позволит нам создать семейство связанных объектов. То есть фабрика деревянных дверей предоставит нам деревянную дверь и эксперта по деревянным дверям. Аналогично для железных дверей:

```kt
interface DoorFactory {
    fun makeDoor(): Door
    fun makeFittingExpert(): DoorFittingExpert
}

// Деревянная фабрика вернет деревянную дверь и столяра
class WoodenDoorFactory : DoorFactory {
    override fun makeDoor(): Door {
        return WoodenDoor()
    }

    override fun makeFittingExpert(): DoorFittingExpert {
        return Carpenter()
    }
}

// Железная фабрика вернет железную дверь и сварщика
class IronDoorFactory : DoorFactory {
    override fun makeDoor(): Door {
        return IronDoor()
    }

    override fun makeFittingExpert(): DoorFittingExpert {
        return Welder()
    }
}
```

Пример использования:

```kt
fun main() {
    var woodenFactory = WoodenDoorFactory()

    var door = woodenFactory.makeDoor()
    var expert = woodenFactory.makeFittingExpert()

    door.getDescription()  // Вывод: Я деревянная дверь
    expert.getDescription() // Вывод: Я работаю только с деревянными дверями

    // Аналогично для железной двери
    var ironFactory = IronDoorFactory()

    door = ironFactory.makeDoor()
    expert = ironFactory.makeFittingExpert()

    door.getDescription()  // Вывод: Я железная дверь
    expert.getDescription() // Вывод: Я работаю только с железными дверями
}
```

Как вы можете заметить, фабрика деревянных дверей инкапсулирует столяра и деревянную дверь, а фабрика железных дверей инкапсулирует железную дверь и слесаря. Это позволило нам убедиться, что для каждой двери мы получим нужного нам установщика.

**Когда использовать**: Когда есть взаимосвязанные зависимости с не очень простой логикой создания.

### Строитель (Builder)

**Строитель** — порождающий шаблон проектирования, который предоставляет способ создания составного объекта. Предназначен для решения проблемы антипаттерна «Телескопический конструктор».

**Пример из жизни**: Представьте, что вы пришли в McDonalds и заказали конкретный продукт, например, БигМак, и вам готовят его без лишних вопросов. Это пример простой фабрики. Но есть случаи, когда логика создания может включать в себя больше шагов. Например, вы хотите индивидуальный сэндвич в Subway: у вас есть несколько вариантов того, как он будет сделан. Какой хлеб вы хотите? Какие соусы использовать? Какой сыр? В таких случаях на помощь приходит шаблон «Строитель».

**Простыми словами**: Шаблон позволяет вам создавать различные виды объекта, избегая засорения конструктора. Он полезен, когда может быть несколько видов объекта или когда необходимо множество шагов, связанных с его созданием.

Давайте я покажу на примере, что такое «Телескопический конструктор». 

```kt
class SomeClass {
    constructor(size: Float, 
                cheese: Boolean = true, 
                pepperoni: Boolean = true, 
                tomato: Boolean = false, 
                lettuce: Boolean = true) {}
}
```    

Как вы можете заметить, количество параметров конструктора может резко увеличиться, и станет сложно понимать расположение параметров. Кроме того, этот список параметров будет продолжать расти, если вы захотите добавить новые варианты. Это и есть «Телескопический конструктор».

Перейдем к примеру в коде. Адекватной альтернативой будет использование шаблона «Строитель». Сначала у нас есть Бутерброд, который мы хотим создать:

```kt
class Burger {
    protected var size: Int? = null
    protected var cheese = false
    protected var pepperoni = false
    protected var lettuce = false
    protected var tomato = false

    constructor(builder: BurgerBuilder)
    {
        size = builder.size
        cheese = builder.cheese
        pepperoni = builder.pepperoni
        lettuce = builder.lettuce
        tomato = builder.tomato
    }
}
```

Аттрибуты бутерброда приватные, мы не будем его разбирать - употребим целиком.

Затем мы берём «Строителя»:

```kt
class BurgerBuilder {
    var size: Int? = null
    var cheese = false
    var pepperoni = false
    var lettuce = false
    var tomato = false

    constructor(_size: Int) {
        size = _size
    }

    fun addPepperoni(): BurgerBuilder {
        pepperoni = true
        return this
    }

    fun addLettuce(): BurgerBuilder {
        lettuce = true
        return this
    }

    fun addCheese(): BurgerBuilder {
        cheese = true
        return this
    }

    fun addTomato(): BurgerBuilder {
        tomato = true
        return this
    }

    fun build(): Burger {
        return Burger(this)
    }
}
```

А вот у строителя аттрибуты публичные, т.к. используются при постронении бутерброда

Пример использования:

```kt
fun main() {
    var burger = BurgerBuilder(14)
        .addPepperoni()
        .addLettuce()
        .addTomato()
        .build()
}
```

**Когда использовать**: Когда может быть несколько видов объекта и надо избежать «телескопического конструктора». Главное отличие от «фабрики» — это то, что она используется, когда создание занимает один шаг, а «строитель» применяется при множестве шагов.

### Прототип (Prototype)

Задаёт виды создаваемых объектов с помощью экземпляра-прототипа и создаёт новые объекты путём копирования этого прототипа. Он позволяет уйти от реализации и позволяет следовать принципу «программирование через интерфейсы». В качестве возвращающего типа указывается интерфейс / абстрактный класс на вершине иерархии, а классы-наследники могут подставить туда наследника, реализующего этот тип.

**Пример из жизни**: Помните Долли? Овечка, которая была клонирована. Не будем углубляться, главное — это то, что здесь все вращается вокруг клонирования.

**Простыми словами**: Прототип создает объект, основанный на существующем объекте при помощи клонирования.

То есть он позволяет вам создавать копию существующего объекта и модернизировать его согласно вашим нуждам, вместо того, чтобы создавать объект заново.

В Котлине легго клонировать объекты наследуя интерфейс **Cloneable** и переопределив его метод *clone()*:

```kt
class Sheep(var name: String) : Cloneable {
    public override fun clone(): Sheep {
        try {
            return super.clone() as Sheep
        } catch(e: CloneNotSupportedException) {
            throw InternalError()
        }
    }
}

fun main() {
    var original = Sheep("Jolly")
    println( original.name ) // Jolly

    // Clone and modify what is required
    var cloned = original.clone()
    cloned.name = "Dolly"
    println(cloned.name) // Dolly
}
```

## Структурные шаблоны

>содрано [отсюда](https://tproger.ru/translations/design-patterns-simple-words-2/)

**Простыми словами**: Структурные шаблоны в основном связаны с композицией объектов, другими словами, с тем, как сущности могут использовать друг друга. Ещё одним объяснением было бы то, что они помогают ответить на вопрос «Как создать программный компонент?».

Список структурных шаблонов проектирования:

* адаптер (Adapter);
* мост (Bridge);
* компоновщик (Composite);
* декоратор (Decorator);
* фасад (Facade);
* приспособленец (Flyweight);
* заместитель (Proxy).

### Адаптер (Adapter)

**Адаптер** — структурный шаблон проектирования, предназначенный для организации использования функций объекта, недоступного для модификации, через специально созданный интерфейс.

**Пример из жизни**: Представим, что у вас на карте памяти есть какие-то изображения и вам надо перенести их на ваш компьютер. Чтобы это сделать, вам нужен какой-то адаптер, который совместим с портами вашего компьютера. В этом случае карт-ридер — это адаптер. Другим примером будет блок питания. Вилку с тремя ножками нельзя вставить в розетку с двумя отверстиями. Для того, чтобы она подошла, надо использовать адаптер. Ещё одним примером будет переводчик, переводящий слова одного человека для другого.

**Простыми словами**: Шаблон позволяет обернуть несовместимые объекты в адаптер, чтобы сделать их совместимыми с другим классом.

Обратимся к коду. Представим игру, в которой охотник охотится на львов.

Изначально у нас есть интерфейс Lion, который реализует всех львов:

```kt
interface Lion {
    fun roar()
}

class AfricanLion : Lion {
    override fun roar(){}
}

class AsianLion : Lion {
    override fun roar(){}
}
```

И Hunter охотится на любую реализацию интерфейса Lion:

```kt
class Hunter {
    fun hunt(lion: Lion){}
}
```

Теперь представим, что нам надо добавить WildDog в нашу игру, на которую наш Hunter также мог бы охотиться. Но мы не можем сделать это напрямую, потому что у WildDog другой интерфейс. Чтобы сделать её совместимой с нашим Hunter, нам надо создать адаптер:

```kt
// Это надо добавить в игру
class WildDog {
    fun bark(){}
}

// Адаптер, чтобы сделать WildDog совместимой с нашей игрой 
class WildDogAdapter(var dog: WildDog) : Lion { 
    override fun roar() { 
        dog.bark() 
    } 
}

fun main() {
    var wildDogAdapter = WildDogAdapter(WildDog())

    var hunter = Hunter()
    hunter.hunt(wildDogAdapter)
}
```

### Мост (Bridge)

**Мост** — структурный шаблон проектирования, используемый в проектировании программного обеспечения чтобы разделять абстракцию и реализацию так, чтобы они могли изменяться независимо. Шаблон мост использует инкапсуляцию, агрегирование и может использовать наследование для того, чтобы разделить ответственность между классами.

**Пример из жизни**: Представим, что у вас есть сайт с разными страницами, и вам надо разрешить пользователям менять их тему. Что вы будете делать? Создавать множественные копии каждой страницы для каждой темы или просто отдельную тему, которую пользователь сможет выбрать сам? Шаблон мост позволяет вам сделать второе.

**Простыми словами**: Шаблон мост — это предпочтение композиции над наследованием. Детали реализации передаются из одной иерархии в другой объект с отдельной иерархией.

Обратимся к примеру в коде. Возьмем пример с нашими страницами. У нас есть иерархия WebPage:

```kt
abstract class WebPage(open var theme: Theme){
    abstract fun getContent(): String
}

class About(override var theme: Theme) : WebPage(theme) {
    override fun getContent(): String = "Страница с информацией в ${theme.getColor()}"
}

class Careers(override var theme: Theme) : WebPage(theme) {
    override fun getContent(): String = "Страница карьеры в ${theme.getColor()}"
}
```

И отдельная иерархия Theme:

```kt
interface Theme {
    fun getColor(): String
}

class DarkTheme : Theme {
    override fun getColor() = "темной теме"
}
class LightTheme : Theme {
    override fun getColor() = "светлой теме"
}

class AquaTheme : Theme {
    override fun getColor() = "голубой теме"
}
```

Применение в коде:

```kt
var darkTheme = DarkTheme()

var about = About(darkTheme)
var careers = Careers(darkTheme)

println(about.getContent()) // "Страница информации в темной теме";
println(careers.getContent()) // "Страница карьеры в темной теме";
```

### Компоновщик (Composite)

**Компоновщик** — структурный шаблон проектирования, объединяющий объекты в древовидную структуру для представления иерархии от частного к целому. Компоновщик позволяет клиентам обращаться к отдельным объектам и к группам объектов одинаково. Паттерн определяет иерархию классов, которые одновременно могут состоять из примитивных и сложных объектов, упрощает архитектуру клиента, делает процесс добавления новых видов объекта более простым.

**Пример из жизни**: Каждая организация скомпонована из сотрудников. У каждого сотрудника есть одинаковые свойства, такие как зарплата, обязанности, отчётность и т.д.

**Простыми словами**: Шаблон компоновщик позволяет клиентам работать с индивидуальными объектами в едином стиле.

Обратимся к коду. Возьмем наш пример с рабочими. У нас есть Employee (работники) разных типов:

```kt
interface Assignee {
    fun canHandleTask(task: String): Boolean
    fun takeTask(task: String)
}

class Employee(val name: String) : Assignee {
    private var hasTask = false
    override fun canHandleTask(task: String) = !hasTask

    override fun takeTask(task: String) {
        println("$name получил задачу: $task")
        hasTask = true
    }
}

class Team(val assignees: ArrayList<Assignee>) : Assignee {

    // вспомогательные методы для управления композитом:
    fun add(assignee: Assignee){
        assignees.add(assignee)
    }
    fun remove(assignee: Assignee){}

    override fun canHandleTask(task: String): Boolean {
        for(assignee in assignees)
            if (assignee.canHandleTask(task)) return true
        return false
    }

    override fun takeTask(task: String) {
        /* может быть разная имплементация - допустим, некоторые задания требуют
        нескольких человек из команды одновременно
        в простейшем случае берем первого незанятого работника среди assignees*/
        var assignee = assignees.removeAt(0)
        assignee.takeTask(task)
    }
}
```

Еще у нас есть Начальник:

```kt
class TaskManager(private val assignees: ArrayList<Assignee>) {
    fun performTask(task: String) {
        for(assignee in assignees)
            if (assignee.canHandleTask(task)) {
                assignee.takeTask(task)
                return
            }

        throw Exception("Cannot handle the task - please hire more people")
    }
}
```

Способ применения (в моей реализации работники "однозадачные"):

```kt
fun main() {
    var employee1 = Employee("трус")
    var employee2 = Employee("балбес")
    var employee3 = Employee("бывалый")
    var employee4 = Employee("шурик")
    var team1 = Team( arrayListOf<Assignee>(employee3, employee4) )

    // ВНИМАНИЕ: передаем команду в taskManager как единый композит.
    // Сам taskManager не знает, что это команда и работает с ней без модификации своей логики.
    var taskManager = TaskManager( arrayListOf<Assignee>(employee1, employee2, team1) )

    for(task in listOf("посадить дерево","построить дом","вырастить сына","украсть невесту","снять фильм"))
        try {
            taskManager.performTask( task )
        } catch (e: Exception){
            println("работники закончились")
            break
        }
}
```

На выходе получим что-то подобное:

```
трус получил задачу: посадить дерево
балбес получил задачу: построить дом
бывалый получил задачу: вырастить сына
шурик получил задачу: украсть невесту
работники закончились
```

### Декоратор (Decorator)

**Декоратор** — структурный шаблон проектирования, предназначенный для динамического подключения дополнительного поведения к объекту. Шаблон декоратор предоставляет гибкую альтернативу практике создания подклассов с целью расширения функциональности.

**Пример из жизни**: Представим, что у вас есть свой кофейный автомат. Он умеет делать только простой кофе, но в двух вариантах: 100 мл и 200 мл. Так как стаканы стандартные, то вам пришла мысль, что для маленькой порции можно добавить опцию "добавить молоко". 

**Простыми словами**: Шаблон декоратор позволяет вам динамически изменять поведение объекта во время работы, оборачивая их в объект класса декоратора.

Перейдем к коду. Возьмем пример с кофе. Изначально у нас есть простой *CoffeeMachine* и реализующий его интерфейс *NormalCoffeeMachine*:

```kt
interface CoffeeMachine {
    fun makeSmallCoffee()
    fun makeLargeCoffee()
}

class NormalCoffeeMachine : CoffeeMachine {
    override fun makeSmallCoffee() = println("обычный: делаю 100 мл")

    override fun makeLargeCoffee() = println("обычный: делаю 200мл")
}
```

Добавляем опцию с молоком:

```kt
//Decorator:
class EnhancedCoffeeMachine(val coffeeMachine: CoffeeMachine) : CoffeeMachine by coffeeMachine {

    // overriding behaviour
    override fun makeLargeCoffee() {
        println("улучшенный: делаю 200 мл")
        coffeeMachine.makeLargeCoffee()
    }

    // extended behaviour
    fun makeCoffeeWithMilk() {
        println("улучшенный: делаю кофе с молоком")
        coffeeMachine.makeSmallCoffee()
        println("улучшенный: добавляю молоко")
    }
}
```

При описании класса *EnhancedCoffeeMachine* мы использовали [делегирование](https://kotlinlang.ru/docs/reference/delegation.html). Раньше мы про него не упоминали: класс Kotlin может реализовать интерфейс, делегируя его методы и свойства другому **объекту**, реализующему этот интерфейс. Это обеспечивает способ создания поведения с использованием ассоциации, а не наследования.

В нашем случае мы в параметрах основного конструктора *EnhancedCoffeeMachine* получаем **экземпляр** класса реализующего интерфейс *CoffeeMachine*, сами тоже говорим, что реализуем интерфейс *CoffeeMachine*, но что-то поручаем делать **объекту** класса: ``CoffeeMachine by coffeeMachine``. И дальше по коду видно, что метод интерфейса *makeSmallCoffee()* в классе не реализован - он вызывается из **экземпляра** класса *NormalCoffeeMachine*. 

А теперь приготовим кофе:

```kt
fun main(){
    val normalMachine = NormalCoffeeMachine()
    val enhancedMachine = EnhancedCoffeeMachine(normalMachine)

    // не переопределенный метод - вызов делегируется
    enhancedMachine.makeSmallCoffee()
    // переопределенный метод со стандартной реализацией
    enhancedMachine.makeLargeCoffee()
    // расширенный метод - добавляем свой функционал
    enhancedMachine.makeCoffeeWithMilk()
}
```

```
обычный: делаю 100 мл
улучшенный: делаю 200 мл
обычный: делаю 200 мл
улучшенный: делаю кофе с молоком
обычный: делаю 100 мл
улучшенный: добавляю молоко
```

### Фасад (Facade)

**Фасад** — структурный шаблон проектирования, позволяющий скрыть сложность системы путём сведения всех возможных внешних вызовов к одному объекту, делегирующему их соответствующим объектам системы.

**Пример из жизни**: Как вы включаете компьютер? Нажимаю на кнопку включения, скажете вы. Это то, во что вы верите, потому что вы используете простой интерфейс, который компьютер предоставляет для доступа снаружи. Внутри же должно произойти гораздо больше вещей. Этот простой интерфейс для сложной подсистемы называется фасадом.

**Простыми словами**: Шаблон фасад предоставляет упрощенный интерфейс для сложной системы.

Перейдем к примерам в коде. 
Изначально у нас есть класс ComplexSystemStore (сложное хранилище) и класс данных, которые нужно сохранять (data class):

```kt
class ComplexSystemStore(val filePath: String) {

    init {
        println("Reading data from file: $filePath")
    }

    val store = HashMap<String, String>()

    fun store(key: String, payload: String) {
        store.put(key, payload)
    }

    fun read(key: String): String = store[key] ?: ""

    fun commit() = println("Storing cached data: $store to file: $filePath")
}

data class User(val login: String)
```

Теперь нарисуем класс *пользовательское хранилище* (фасад).

```kt
//Facade:
class UserRepository {
    val systemPreferences = ComplexSystemStore("/data/default.prefs")

    fun save(user: User) {
        systemPreferences.store("USER_KEY", user.login)
        systemPreferences.commit()
    }

    fun findFirst(): User = User(systemPreferences.read("USER_KEY"))
}
```

Пример использования:

```kt
fun main(){
    val userRepository = UserRepository()
    val user = User("dbacinski")
    userRepository.save(user)
    val resultUser = userRepository.findFirst()
    println("Found stored user: $resultUser")
}
```

```
Reading data from file: /data/default.prefs
Storing cached data: {USER_KEY=dbacinski} to file: /data/default.prefs
Found stored user: User(login=dbacinski)
```

Таким образом мы скрываем от пользователя внутреннюю реализацию хранилища, пользователь имеет только две *крутилки*: сохранить и найти.

### Приспособленец (Flyweight)

**Приспособленец** — структурный шаблон проектирования, при котором объект, представляющий себя как уникальный экземпляр в разных местах программы, по факту не является таковым.

**Пример из жизни**: Вы когда-нибудь заказывали чай в уличном ларьке? Там зачастуют готовят не одну чашку, которую вы заказали, а гораздо большую емкость. Это делается для того, чтобы экономить ресурсы (газ/электричество). Газ/электричество в этом примере и являются приспособленцами, ресурсы которых делятся (sharing).

**Простыми словами**: Приспособленец используется для минимизации использования памяти или вычислительной стоимости путем разделения ресурсов с наибольшим количеством похожих объектов.

Перейдем к примерам в коде. Возьмем наш пример с чаем. Изначально у нас есть различные виды Tea и TeaMaker:

//TODO: добавить интерфейс Tea и несколько классов чая. Сделать уменьшение ресурса при заказе

```kt
// Все, что будет закешировано, является приспособленцем.
// Типы чая здесь будут приспособленцами.
class KarakTea

//Ведет себя как фабрика и сохраняет чай
class TeaMaker {
    protected var availableTea = mutableMapOf<String, KarakTea>()

    fun make(preference: String): KarakTea {
        if(!availableTea.containsKey(preference))
            availableTea.put(preference, KarakTea())

        return availableTea[preference]!!
    }
}
```

Теперь у нас есть TeaShop, который принимает заказы и выполняет их:

```kt
class TeaShop(val teaMaker: TeaMaker) {
    protected var orders = mutableMapOf<Int, KarakTea>()

    fun takeOrder(teaType: String, table: Int) {
        orders.put(table, teaMaker.make(teaType))
    }

    fun serve() {
        for ((table, tea) in orders)
            println("Serving tea ($tea) to table $table")
    }
}
```

Пример использования:

```kt
fun main(){
    var shop = TeaShop( TeaMaker() );

    shop.takeOrder("меньше сахара", 1)
    shop.takeOrder("больше молока", 2)
    shop.takeOrder("без сахара", 5)

    shop.serve()
}
```

В консоли получим примерно такое:

```
Serving tea (KarakTea@12edcd21) to table 1
Serving tea (KarakTea@34c45dca) to table 2
Serving tea (KarakTea@52cc8049) to table 5
```

### Заместитель (Proxy)

**Заместитель** — структурный шаблон проектирования, который предоставляет объект, который контролирует доступ к другому объекту, перехватывая все вызовы (выполняет функцию контейнера).

**Пример из жизни**: Вы когда-нибудь использовали карту доступа, чтобы пройти через дверь? Есть несколько способов открыть дверь: например, она может быть открыта при помощи карты доступа или нажатия кнопки, которая обходит защиту. Основная функциональность двери — это открытие, но заместитель, добавленный поверх этого, добавляет функциональность. Но лучше я объясню это на примере кода чуть ниже.

**Простыми словами**: Используя шаблон заместитель, класс отображает функциональность другого класса.

Перейдем к коду. Возьмем наш пример с безопасностью. Сначала у нас есть интерфейс Дверь и его реализация:

```kt
interface Door {
    fun open()
    fun close()
}

class LabDoor : Door {
    override fun open() = println( "Открытие дверь лаборатории" )
    override fun close() = println( "Закрытие двери лаборатории" )
}
```

Затем у нас есть заместитель Security для защиты любых наших дверей:

```kt
class Security(val door: Door) {
    fun open(password: String) {
        if (authenticate(password))
            door.open()
        else
            println( "Нет! Это невозможно." )
    }

    private fun authenticate(password: String) = password.equals("Secr@t")

    fun close() {
        door.close()
    }
}
```

Пример использования:

```kt
fun main() {
    var door = Security( LabDoor() )
    door.open("invalid")    // Нет! Это невозможно.

    door.open("Secr@t")     // Открытие двери лаборатории
    door.close() // Закрытие двери лаборатории
}
```

> Пример простой и из него не понятно, почему бы классу Security просто не наследоваться от LabDoor и переопределить метод open. Но нужно учитывать, что дверей в здании может быть несколько и варианты доступа могут отличаться для разных типов (классов) дверей.


## Поведенческие шаблоны

>содрано [отсюда](https://tproger.ru/translations/design-patterns-simple-words-3/) с переводом на Котлин и проверкой

Поведенческие шаблоны связаны с распределением обязанностей между объектами. Их отличие от структурных шаблонов заключается в том, что они не просто описывают структуру, но также описывают шаблоны для передачи сообщений / связи между ними. Или, другими словами, они помогают ответить на вопрос «Как запустить поведение в программном компоненте?»

**Поведенческие шаблоны** — шаблоны проектирования, определяющие алгоритмы и способы реализации взаимодействия различных объектов и классов.

Поведенческие шаблоны:

* цепочка обязанностей (Chain of Responsibility);
* команда (Command);
* итератор (Iterator);
* посредник (Mediator);
* хранитель (Memento);
* наблюдатель (Observer);
* посетитель (Visitor);
* стратегия (Strategy);
* состояние (State);
* шаблонный метод (Template Method).

### Цепочка обязанностей (Chain of Responsibility)

**Цепочка обязанностей** — поведенческий шаблон проектирования предназначенный для организации в системе уровней ответственности.

**Пример из жизни**: Король орков отдает громкие приказы своей армии. Сначала реагирует командир, затем офицер, а затем солдат. Командир, офицер и солдат здесь образуют цепь ответственности.

**Простыми словами**: цепочка обязанностей помогает строить цепочки объектов. Запрос входит с одного конца и проходит через каждый объект, пока не найдет подходящий обработчик.

Обратимся к коду. 
Приведем пример с формированием заголовка http-запроса. 

Есть интерфейс *Цепочка Заголовков* и два класса, реализующих этот интерфейс.


```kt
interface HeadersChain {
    fun addHeader(inputHeader: String): String
}

class AuthenticationHeader(val token: String?,
                           var next: HeadersChain? = null) : HeadersChain {

    override fun addHeader(inputHeader: String): String {
        token ?: throw IllegalStateException("Token should be not null")
        return inputHeader + "Authorization: Bearer $token\n"
            .let { next?.addHeader(it) ?: it }
    }
}

class ContentTypeHeader(val contentType: String,
                        var next: HeadersChain? = null) : HeadersChain {

    override fun addHeader(inputHeader: String): String =
        inputHeader + "ContentType: $contentType\n"
            .let { next?.addHeader(it) ?: it }
}
```

Также есть класс для формирования тела запроса:

```kt
class BodyPayload(val body: String,
                  var next: HeadersChain? = null) : HeadersChain {

    override fun addHeader(inputHeader: String): String =
        inputHeader + "$body"
            .let { next?.addHeader(it) ?: it }
}
```

Пример использования:

```kt
// создаем элементы цепочки
val authenticationHeader = AuthenticationHeader("123456")
val contentTypeHeader = ContentTypeHeader("json")
val messageBody = BodyPayload("Body:\n{\n\"username\"=\"dbacinski\"\n}")

// формируем цепочку
authenticationHeader.next = contentTypeHeader
contentTypeHeader.next = messageBody

// формируем запрос с авторизацией
val messageWithAuthentication =
    authenticationHeader.addHeader("Headers with Authentication:\n")
println(messageWithAuthentication)

// формируем запрос без авторизации
val messageWithoutAuth =
    contentTypeHeader.addHeader("Headers:\n")
println(messageWithoutAuth)
```

```
Headers with Authentication:
Authorization: Bearer 123456
ContentType: json
Body:
{
"username"="dbacinski"
}

Headers without Authentication:
ContentType: json
Body:
{
"username"="dbacinski"
}
```

### Команда (Command)

**Команда** — поведенческий шаблон проектирования, используемый при объектно-ориентированном программировании, представляющий действие. Объект команды заключает в себе само действие и его параметры.

**Пример из жизни**: Типичный пример: вы заказываете еду в ресторане. Вы (т.е. Client) просите официанта (например, Invoker) принести еду (то есть Command), а официант просто переправляет запрос шеф-повару (то есть Receiver), который знает, что и как готовить. Другим примером может быть то, что вы (Client) включаете (Command) телевизор (Receiver) с помощью пульта дистанционного управления (Invoker).

**Простыми словами**: Позволяет вам инкапсулировать действия в объекты. Основная идея, стоящая за шаблоном — это предоставление средств, для разделения клиента и получателя.

Обратимся к коду. Изначально у нас есть получатель Bulb (лампочка), в котором есть реализация каждого действия, которое может быть выполнено:

```kt
// Получатель
class Bulb {
    fun turnOn() = println("Лампочка загорелась")
    fun turnOff() = println("Темнота!")
}
```

Затем у нас есть интерфейс Command, c набором команд:

```kt
interface Command {
    fun execute()
    fun undo()
    fun redo()
}
```

И классы, реализующие эти команды:

```kt
// Команда
class TurnOn(protected var bulb: Bulb) : Command {
    override fun execute() = bulb.turnOn()
    override fun undo() = bulb.turnOff()
    override fun redo() = execute()
}

class TurnOff(protected var bulb: Bulb) : Command {
    override fun execute() = bulb.turnOff()
    override fun undo() = bulb.turnOn()
    override fun redo() = execute()
}
```

И у нас есть Пульт, с которым клиент будет взаимодействовать для обработки любых команд:

```kt
// Invoker
class RemoteControl {
    fun submit(command: Command) = command.execute()
}
```

Наконец, мы можем увидеть, как использовать нашего клиента:

```kt
fun main() {
    var bulb = Bulb()

    var turnOn = TurnOn(bulb)
    var turnOff = TurnOff(bulb)

    var remote = RemoteControl()
    remote.submit(turnOn)   // Лампочка загорелась!
    remote.submit(turnOff)  // Темнота!
}
```

Шаблон **команда** может быть использован для реализации системы, основанной на транзакциях, где вы сохраняете историю команд, как только их выполняете. Если окончательная команда успешно выполнена, то все хорошо, иначе алгоритм просто перебирает историю и продолжает выполнять отмену для всех выполненных команд.

### Итератор

**Итератор** — поведенческий шаблон проектирования. Представляет собой объект, позволяющий получить последовательный доступ к элементам объекта-агрегата без использования описаний каждого из агрегированных объектов.

Что-то не нашел примера под котлин, но вообще в котлине есть интерфейс Iterable и такой шаблон как-то отдельно реализовывать не нужно.


### Посредник (Mediator)

**Посредник** — поведенческий шаблон проектирования, обеспечивающий взаимодействие множества объектов, формируя при этом слабую связанность, и избавляя объекты, от необходимости явно ссылаться друг на друга.

**Пример из жизни**: Общим примером будет, когда вы говорите с кем-то по мобильнику, то между вами и собеседником находится мобильный оператор. То есть сигнал передаётся через него, а не напрямую. В данном примере оператор — посредник.

**Простыми словами**: Шаблон посредник подразумевает добавление стороннего объекта (посредника) для управления взаимодействием между двумя объектами (коллегами). Шаблон помогает уменьшить связанность (coupling) классов, общающихся друг с другом, ведь теперь они не должны знать о реализациях своих собеседников.

Разберем пример в коде. Простейший пример: чат (посредник), в котором пользователи отправляют друг другу сообщения.

Изначально у нас есть посредник ChatMediator:

```kt
class ChatMediator {

    private val users: MutableList<ChatUser> = ArrayList()

    fun sendMessage(msg: String, user: ChatUser) {
        users
            .filter { it != user }
            .forEach {
                it.receive(msg)
            }
    }

    fun addUser(user: ChatUser): ChatMediator =
        apply { users.add(user) }

}
```

И собственно пользователи чата (User):

```kt
class ChatUser(private val mediator: ChatMediator, val name: String) {
    fun send(msg: String) {
        println("$name: Sending Message= $msg")
        mediator.sendMessage(msg, this)
    }

    fun receive(msg: String) {
        println("$name: Message received: $msg")
    }
}
```

Пример использования:

```kt
val mediator = ChatMediator()
val john = ChatUser(mediator, "John")

mediator
    .addUser(ChatUser(mediator, "Alice"))
    .addUser(ChatUser(mediator, "Bob"))
    .addUser(john)
john.send("Hi everyone!")
```

```
John: Sending Message= Hi everyone!
Alice: Message received: Hi everyone!
Bob: Message received: Hi everyone!
```

### Хранитель (Memento)

**Хранитель** — поведенческий шаблон проектирования, позволяющий, не нарушая инкапсуляцию, зафиксировать и сохранить внутреннее состояние объекта так, чтобы позднее восстановить его в этом состоянии.

**Пример из жизни**: В качестве примера можно привести калькулятор (создатель), у которого любая последняя выполненная операция сохраняется в памяти (хранитель), чтобы вы могли снова вызвать её с помощью каких-то кнопок (опекун).

**Простыми словами**: Шаблон хранитель фиксирует и хранит текущее состояние объекта, чтобы оно легко восстанавливалось.

Обратимся к коду. Возьмем наш пример текстового редактора, который время от времени сохраняет состояние, которое вы можете восстановить.

```kt
// класс данных для сериализации состояния
data class Memento(val state: String)

class Originator(var state: String) {
    fun createMemento() = Memento(state)

    fun restore(memento: Memento) {
        state = memento.state
    }
}

class CareTaker {
    private val mementoList = ArrayList<Memento>()

    fun saveState(state: Memento) {
        mementoList.add(state)
    }

    fun restore(index: Int): Memento {
        return mementoList[index]
    }
}
```

Пример использования:


```kt
val originator = Originator("initial state")
val careTaker = CareTaker()

careTaker.saveState(originator.createMemento())

originator.state = "State #1"
originator.state = "State #2"

careTaker.saveState(originator.createMemento())

originator.state = "State #3"
println("Current State: " + originator.state)

originator.restore(careTaker.restore(1))
println("Second saved state: " + originator.state)

originator.restore(careTaker.restore(0))
println("First saved state: " + originator.state)
```

```
Current State: State #3
Second saved state: State #2
First saved state: initial state
```

### Наблюдатель (Observer)

**Наблюдатель** — поведенческий шаблон проектирования, также известен как «подчинённые» (Dependents). Создает механизм у класса, который позволяет получать экземпляру объекта этого класса оповещения от других объектов об изменении их состояния, тем самым наблюдая за ними.

**Пример из жизни**: Хороший пример: люди, ищущие работу, подписываются на публикации на сайтах вакансий и получают уведомления, когда появляются вакансии подходящие по параметрам.

**Простыми словами**: Шаблон определяет зависимость между объектами, чтобы при изменении состояния одного из них зависимые от него узнавали об этом.

```kt
import kotlin.properties.Delegates

// интерфейс для подписчиков
interface TextChangedListener {
    fun onTextChanged(oldText: String, newText: String)
}

// класс подписчика
class PrintingTextChangedListener : TextChangedListener {
    // при получении уведомления выведет сообщение
    override fun onTextChanged(oldText: String, newText: String) {
        println("Text is changed: \"$oldText\" -> \"$newText\"")
    }
}

// класс, поддерживающий подписку
class TextView {
    // список подписчиков
    private val listeners = mutableListOf<TextChangedListener>()

    // сеттер для добавления подписчиков в список
    var listener: TextChangedListener? = null
        set(value){
            if(value!=null) listeners.add(value)
        }


    // Delegates.observable() при изменении свойства выполняет лямбда-функцию
    var text: String by Delegates.observable("<empty>") { _, old, new ->
        listeners.forEach { 
            it.onTextChanged(old, new) 
        }
    }
}
```

>В этом примере можно обойтись без делегата, сделав сеттер для поля *text*:
>
>```kt
>    var text = ""
>        set(value){
>            if(!text.equals(value)){
>                listeners.forEach { it.onTextChanged(text, value) }
>                field = value
>            }
>        }
>```
>
>Здесь *field* - это так называемое **теневое** имя текущего свойства, если бы его не было, то программа попала бы в бесконечную рекурсю при попытке сохранить новое значение внутри сеттера.

Ну и проверим как работает наш код:

```kt
val textView = TextView()

// добавляем экземпляр подписчика
textView.listener = PrintingTextChangedListener()

// меняем свойство text
with(textView) {
    text = "Lorem ipsum"
    text = "dolor sit amet"
}
```

```
Text is changed: "" -> "Lorem ipsum"
Text is changed: "Lorem ipsum" -> "dolor sit amet"
```

### Посетитель (Visitor)

**Посетитель** — поведенческий шаблон проектирования, описывающий операцию, которая выполняется над объектами других классов. При изменении *visitor* нет необходимости изменять обслуживаемые классы.

**Пример из жизни**: Туристы собрались в Дубай. Сначала им нужен способ попасть туда (виза). После прибытия они будут посещать любую часть города, не спрашивая разрешения ходить где вздумается. Просто скажите им о каком-нибудь месте — и туристы могут там побывать. Шаблон посетитель помогает добавлять места для посещения.

**Простыми словами**: Шаблон посетитель позволяет добавлять будущие операции для объектов без их модифицирования.

//TODO: расписать что делает код

```kt
interface ReportVisitable {
    fun <R> accept(visitor: ReportVisitor<R>): R
}

class FixedPriceContract(val costPerYear: Long) : ReportVisitable {
    override fun <R> accept(visitor: ReportVisitor<R>): R = visitor.visit(this)
}

class TimeAndMaterialsContract(val costPerHour: Long, val hours: Long) : ReportVisitable {
    override fun <R> accept(visitor: ReportVisitor<R>): R = visitor.visit(this)
}

class SupportContract(val costPerMonth: Long) : ReportVisitable {
    override fun <R> accept(visitor: ReportVisitor<R>): R = visitor.visit(this)
}

interface ReportVisitor<out R> {
    fun visit(contract: FixedPriceContract): R
    fun visit(contract: TimeAndMaterialsContract): R
    fun visit(contract: SupportContract): R
}

class MonthlyCostReportVisitor : ReportVisitor<Long> {
    override fun visit(contract: FixedPriceContract): Long =
        contract.costPerYear / 12

    override fun visit(contract: TimeAndMaterialsContract): Long =
        contract.costPerHour * contract.hours

    override fun visit(contract: SupportContract): Long =
        contract.costPerMonth
}

class YearlyReportVisitor : ReportVisitor<Long> {
    override fun visit(contract: FixedPriceContract): Long =
        contract.costPerYear

    override fun visit(contract: TimeAndMaterialsContract): Long =
        contract.costPerHour * contract.hours

    override fun visit(contract: SupportContract): Long =
        contract.costPerMonth * 12
}
```

Пример работы:

```kt
fun main() {
    val projects = arrayOf(
        FixedPriceContract(costPerYear = 10000),
        TimeAndMaterialsContract(hours = 150, costPerHour = 10),
        SupportContract(costPerMonth = 500),
        TimeAndMaterialsContract(hours = 50, costPerHour = 50))

    val monthlyCostReportVisitor = MonthlyCostReportVisitor()

    val monthlyCost = projects.map { it.accept(monthlyCostReportVisitor) }.sum()
    println("Monthly cost: $monthlyCost")

    val yearlyReportVisitor = YearlyReportVisitor()
    val yearlyCost = projects.map { it.accept(yearlyReportVisitor) }.sum()
    println("Yearly cost: $yearlyCost")
}
```

```
Monthly cost: 5333
Yearly cost: 20000
```

### Стратегия (Strategy)

**Стратегия** — поведенческий шаблон проектирования, предназначенный для определения семейства алгоритмов, инкапсуляции каждого из них и обеспечения их взаимозаменяемости. Это позволяет выбирать алгоритм путём определения соответствующего класса. Шаблон Strategy позволяет менять выбранный алгоритм независимо от объектов-клиентов, которые его используют.

**Пример из жизни**: Возьмём пример с пузырьковой сортировкой. Мы её реализовали, но с ростом объёмов данных сортировка работа стала выполняться очень медленно. Тогда мы сделали быструю сортировку. Алгоритм работает быстрее на больших объёмах, но на маленьких он очень медленный. Тогда мы реализовали стратегию, при которой для маленьких объёмов данных используется пузырьковая сортировка, а для больших объёмов — быстрая.

**Простыми словами**: Шаблон стратегия позволяет переключаться между алгоритмами или стратегиями в зависимости от ситуации.

В примере класс для вывода (печати) строки принимающий в параметрах лямбда-функцию (стратегию) для предварительно обработки этой строки.

```kt
class Printer(private val stringFormatterStrategy: (String) -> String) {
    fun printString(string: String) {
        println(stringFormatterStrategy(string))
    }
}

val lowerCaseFormatter: (String) -> String = { it.toLowerCase() }
val upperCaseFormatter = { it: String -> it.toUpperCase() }
```

Пример использования:

```kt
fun main() {
    val inputString = "LOREM ipsum DOLOR sit amet"

    val lowerCasePrinter = Printer(lowerCaseFormatter)
    lowerCasePrinter.printString(inputString)

    val upperCasePrinter = Printer(upperCaseFormatter)
    upperCasePrinter.printString(inputString)

    val prefixPrinter = Printer { "Prefix: $it" }
    prefixPrinter.printString(inputString)
}
```

```
lorem ipsum dolor sit amet
LOREM IPSUM DOLOR SIT AMET
Prefix: LOREM ipsum DOLOR sit amet
```

### Состояние (State)

**Состояние** — поведенческий шаблон проектирования. Используется в тех случаях, когда во время выполнения программы объект должен менять своё поведение в зависимости от своего состояния.

**Пример из жизни**: Допустим, в графическом редакторе вы выбрали кисть. Она меняет своё поведение в зависимости от настройки цвета, т. е. рисует линию выбранного цвета.

**Простыми словами**: Шаблон позволяет менять поведение класса при изменении состояния.

Перейдем к примерам в коде.
Есть класс для авторизации пользователей (AuthorizationPresenter) и классы для состояния авторизайии: Unauthorized, Authorized. 

```kt
// изолированный класс - все его наследники должны быть объявлены в этом же файле
sealed class AuthorizationState

// object создает экземпляр и класс одновременно
object Unauthorized : AuthorizationState()

class Authorized(val userName: String) : AuthorizationState()

class AuthorizationPresenter {

    private var state: AuthorizationState = Unauthorized

    val isAuthorized: Boolean
        get() = when (state) {
            is Authorized -> true
            is Unauthorized -> false
        }

    val userName: String
        get() {
            val state = this.state //val enables smart casting of state
            return when (state) {
                is Authorized -> state.userName
                is Unauthorized -> "Unknown"
            }
        }

    fun loginUser(userName: String) {
        state = Authorized(userName)
    }

    fun logoutUser() {
        state = Unauthorized
    }

    override fun toString() = "User '$userName' is logged in: $isAuthorized"
}
```

Пример работы:

```kt
fun main() {
    val authorizationPresenter = AuthorizationPresenter()

    authorizationPresenter.loginUser("admin")
    println(authorizationPresenter)

    authorizationPresenter.logoutUser()
    println(authorizationPresenter)
}
```

```
User 'admin' is logged in: true
User 'Unknown' is logged in: false
```

### Шаблонный метод (Template Method)

**Шаблонный метод** — поведенческий шаблон проектирования, определяющий основу алгоритма и позволяющий наследникам переопределять некоторые шаги алгоритма, не изменяя его структуру в целом.

**Пример из жизни**: Допустим, вы собрались строить дома. Этапы будут такими:

* Подготовка фундамента.
* Возведение стен.
* Настил крыши.
* Настил перекрытий.

Порядок этапов никогда не меняется. Вы не настелите крышу до возведения стен и т. д. Но каждый этап модифицируется: стены, например, можно возвести из дерева, кирпича или газобетона.

**Простыми словами**: Шаблонный метод определяет каркас выполнения определённого алгоритма, но реализацию самих этапов делегирует дочерним классам.

Обратимся к коду. Допустим, у нас есть программный инструмент, позволяющий тестировать, проводить контроль качества кода, выполнять сборку, генерировать отчёты сборки (отчёты о покрытии кода, о качестве кода и т. д.), а также развёртывать приложение на тестовом сервере.

Изначально у нас есть наш Builder, который описывает скелет для построения алгоритма:

```kt
abstract class Builder {
    // Шаблонный метод
    fun build() {
        test()
        lint()
        assemble()
        deploy()
    }

    abstract fun test()
    abstract fun lint()
    abstract fun assemble()
    abstract fun deploy()
}
```

Затем у нас есть его реализации:

```kt
class AndroidBuilder : Builder() {
    override fun test() = println("Запуск Android тестов")
    override fun lint() = println("Копирование Android кода")
    override fun assemble() = println("Android сборка")
    override fun deploy() = println("Развертывание сборки на сервере")
}

class IosBuilder : Builder() {
    override fun test() = println("Запуск iOS тестов")
    override fun lint() = println("Копирование iOS кода")
    override fun assemble() = println("iOS сборка")
    override fun deploy() = println("Развертывание сборки на сервере")
}
```

Пример использования:

```kt
fun main() {
    var androidBuilder = AndroidBuilder()
    androidBuilder.build()

    var iosBuilder = IosBuilder()
    iosBuilder.build()
}
```

```
Запуск Android тестов
Копирование Android кода
Android сборка
Развертывание сборки на сервере
Запуск iOS тестов
Копирование iOS кода
iOS сборка
Развертывание сборки на сервере
```

<table style="width: 100%;"><tr><td style="width: 40%;">
<a href="../articles/t6_linq.md">LINQ
</a></td><td style="width: 20%;">
<a href="../readme.md">Содержание
</a></td><td style="width: 40%;">
<a href="../articles/t7_dll.md">Библиотеки классов
</a></td><tr></table>
