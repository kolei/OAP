[содержание](/readme.md)  

# Структурные шаблоны

>содрано [отсюда](https://tproger.ru/translations/design-patterns-simple-words-2/) с переводом на Котлин и проверкой

>[реализации на котлин](https://github.com/dbacinski/Design-Patterns-In-Kotlin#decorator)

**Простыми словами**: Структурные шаблоны в основном связаны с композицией объектов, другими словами, с тем, как сущности могут использовать друг друга. Ещё одним объяснением было бы то, что они помогают ответить на вопрос «Как создать программный компонент?».

Список структурных шаблонов проектирования:

* адаптер (Adapter);
* мост (Bridge);
* компоновщик (Composite);
* декоратор (Decorator);
* фасад (Facade);
* приспособленец (Flyweight);
* заместитель (Proxy).

## Адаптер (Adapter)

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

## Мост (Bridge)

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

## Компоновщик (Composite)

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

## Декоратор (Decorator)

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

## Фасад (Facade)

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

## Приспособленец (Flyweight)

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

## Заместитель (Proxy)

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

[содержание](/readme.md)  


[_]: https://refactoring.guru/ru/design-patterns/bridge