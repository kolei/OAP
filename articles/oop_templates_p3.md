[содержание](/readme.md)  

# Поведенческие шаблоны

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

## Цепочка обязанностей (Chain of Responsibility)

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

## Команда (Command)

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

## Итератор

**Итератор** — поведенческий шаблон проектирования. Представляет собой объект, позволяющий получить последовательный доступ к элементам объекта-агрегата без использования описаний каждого из агрегированных объектов.

Что-то не нашел примера под котлин, но вообще в котлине есть интерфейс Iterable и такой шаблон как-то отдельно реализовывать не нужно.


## Посредник (Mediator)

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

## Хранитель (Memento)

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

## Наблюдатель (Observer)

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

## Посетитель (Visitor)

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

## Стратегия (Strategy)

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

## Состояние (State)

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

## Шаблонный метод (Template Method)

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

[содержание](/readme.md)  
