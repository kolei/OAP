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

//TODO: остановился тут


```kt
// интерфейс для наблюдателя
interface TextChangedListener {
    fun onTextChanged(oldText: String, newText: String)
}

// класс, 
class PrintingTextChangedListener : TextChangedListener {
    
    private var text = ""
    
    override fun onTextChanged(oldText: String, newText: String) {
        text = "Text is changed: $oldText -> $newText"
    }
}

class TextView {

    val listeners = mutableListOf<TextChangedListener>()

    var text: String by Delegates.observable("<empty>") { _, old, new ->
        listeners.forEach { it.onTextChanged(old, new) }
    }
}
```



Посетитель (Visitor)
Википедия гласит:

Посетитель — поведенческий шаблон проектирования, описывающий операцию, которая выполняется над объектами других классов. При изменении visitor нет необходимости изменять обслуживаемые классы.

Пример из жизни: Туристы собрались в Дубай. Сначала им нужен способ попасть туда (виза). После прибытия они будут посещать любую часть города, не спрашивая разрешения ходить где вздумается. Просто скажите им о каком-нибудь месте — и туристы могут там побывать. Шаблон посетитель помогает добавлять места для посещения.

Простыми словами: Шаблон посетитель позволяет добавлять будущие операции для объектов без их модифицирования.

Перейдем к примерам в коде. Возьмём зоопарк: у нас есть несколько видов Animal, и нам нужно послушать издаваемые ими звуки.

// Посещаемый
interface Animal
{
    public function accept(AnimalOperation $operation);
}

// Посетитель
interface AnimalOperation
{
    public function visitMonkey(Monkey $monkey);
    public function visitLion(Lion $lion);
    public function visitDolphin(Dolphin $dolphin);
}
Затем у нас есть реализация для животных:

class Monkey implements Animal
{
    public function shout()
    {
        echo 'У-у-а-а!';
    }

    public function accept(AnimalOperation $operation)
    {
        $operation->visitMonkey($this);
    }
}

class Lion implements Animal
{
    public function roar()
    {
        echo 'рррр!';
    }

    public function accept(AnimalOperation $operation)
    {
        $operation->visitLion($this);
    }
}

class Dolphin implements Animal
{
    public function speak()
    {
        echo '*звуки дельфина*!'; // Я понятия не имею как описать их звуки
    }

    public function accept(AnimalOperation $operation)
    {
        $operation->visitDolphin($this);
    }
}
Давайте реализуем посетителя:

class Speak implements AnimalOperation
{
    public function visitMonkey(Monkey $monkey)
    {
        $monkey->shout();
    }

    public function visitLion(Lion $lion)
    {
        $lion->roar();
    }

    public function visitDolphin(Dolphin $dolphin)
    {
        $dolphin->speak();
    }
}
Пример использования:

$monkey = new Monkey();
$lion = new Lion();
$dolphin = new Dolphin();

$speak = new Speak();

$monkey->accept($speak);    // У-у-а-а!    
$lion->accept($speak);      // Рррр!
$dolphin->accept($speak);   // *звуки дельфина*!
Это можно было сделать просто с помощью иерархии наследования, но тогда пришлось бы модифицировать животных при каждом добавлении к ним новых действий. А здесь менять их не нужно. Например, мы можем добавить животным прыжки, просто создав нового посетителя:

class Jump implements AnimalOperation
{
    public function visitMonkey(Monkey $monkey)
    {
        echo 'Прыгает на 20 футов!';
    }

    public function visitLion(Lion $lion)
    {
        echo 'Прыгает на 7 футов!';
    }

    public function visitDolphin(Dolphin $dolphin)
    {
        echo 'Появился над водой и исчез!';
    }
}
Пример использования:

$jump = new Jump();

$monkey->accept($speak);   // У-у-а-а!
$monkey->accept($jump);    // Прыгает на 20 футов!

$lion->accept($speak);     // Рррр!
$lion->accept($jump);      // Прыгает на 7 футов!

$dolphin->accept($speak);  // *звуки дельфинов*!
$dolphin->accept($jump);   // Появился над водой и исчез

Примеры на Java и Python.

Стратегия (Strategy)
Википедия гласит:

Стратегия — поведенческий шаблон проектирования, предназначенный для определения семейства алгоритмов, инкапсуляции каждого из них и обеспечения их взаимозаменяемости. Это позволяет выбирать алгоритм путём определения соответствующего класса. Шаблон Strategy позволяет менять выбранный алгоритм независимо от объектов-клиентов, которые его используют.

Пример из жизни: Возьмём пример с пузырьковой сортировкой. Мы её реализовали, но с ростом объёмов данных сортировка работа стала выполняться очень медленно. Тогда мы сделали быструю сортировку. Алгоритм работает быстрее на больших объёмах, но на маленьких он очень медленный. Тогда мы реализовали стратегию, при которой для маленьких объёмов данных используется пузырьковая сортировка, а для больших объёмов — быстрая.

Простыми словами: Шаблон стратегия позволяет переключаться между алгоритмами или стратегиями в зависимости от ситуации.

Перейдем к коду. Возьмем наш пример. Изначально у нас есть наша SortStrategy и разные её реализации:

interface SortStrategy
{
    public function sort(array $dataset): array;
}

class BubbleSortStrategy implements SortStrategy
{
    public function sort(array $dataset): array
    {
        echo "Сортировка пузырьком";

        // Сортировка
        return $dataset;
    }
}

class QuickSortStrategy implements SortStrategy
{
    public function sort(array $dataset): array
    {
        echo "Быстрая сортировка";

        // Сортировка
        return $dataset;
    }
}
И у нас есть Sorter, который собирается использовать какую-то стратегию:

class Sorter
{
    protected $sorter;

    public function __construct(SortStrategy $sorter)
    {
        $this->sorter = $sorter;
    }

    public function sort(array $dataset): array
    {
        return $this->sorter->sort($dataset);
    }
}
Пример использования:

$dataset = [1, 5, 4, 3, 2, 8];

$sorter = new Sorter(new BubbleSortStrategy());
$sorter->sort($dataset); // Вывод : Сортировка пузырьком

$sorter = new Sorter(new QuickSortStrategy());
$sorter->sort($dataset); // Вывод : Быстрая сортировка

Примеры на Java и Python.

Состояние (State)
Википедия гласит:

Состояние — поведенческий шаблон проектирования. Используется в тех случаях, когда во время выполнения программы объект должен менять своё поведение в зависимости от своего состояния.

Пример из жизни: Допустим, в графическом редакторе вы выбрали кисть. Она меняет своё поведение в зависимости от настройки цвета, т. е. рисует линию выбранного цвета.

Простыми словами: Шаблон позволяет менять поведение класса при изменении состояния.

Перейдем к примерам в коде. Возьмем пример текстового редактора, он позволяет вам менять состояние напечатанного текста. Например, если у вас выбран курсив, то он будет писать курсивом и так далее.

Изначально у нас есть интерфейс WritingState и несколько его реализаций:

interface WritingState
{
    public function write(string $words);
}

class UpperCase implements WritingState
{
    public function write(string $words)
    {
        echo strtoupper($words);
    }
}

class LowerCase implements WritingState
{
    public function write(string $words)
    {
        echo strtolower($words);
    }
}

class Default implements WritingState
{
    public function write(string $words)
    {
        echo $words;
    }
}
Затем TextEditor:

class TextEditor
{
    protected $state;

    public function __construct(WritingState $state)
    {
        $this->state = $state;
    }

    public function setState(WritingState $state)
    {
        $this->state = $state;
    }

    public function type(string $words)
    {
        $this->state->write($words);
    }
}
Пример использования:

$editor = new TextEditor(new Default());

$editor->type('Первая строка');

$editor->setState(new UpperCase());

$editor->type('Вторая строка');
$editor->type('Третья строка');

$editor->setState(new LowerCase());

$editor->type('Четвертая строка');
$editor->type('Пятая строка');

// Output:
// Первая строка
// ВТОРАЯ СТРОКА
// ТРЕТЬЯ СТРОКА
// четвертая строка
// пятая строка

Примеры на Java и Python.

Шаблонный метод (Template Method)
Википедия гласит:

Шаблонный метод — поведенческий шаблон проектирования, определяющий основу алгоритма и позволяющий наследникам переопределять некоторые шаги алгоритма, не изменяя его структуру в целом.

Пример из жизни: Допустим, вы собрались строить дома. Этапы будут такими:

Подготовка фундамента.
Возведение стен.
Настил крыши.
Настил перекрытий.
Порядок этапов никогда не меняется. Вы не настелите крышу до возведения стен и т. д. Но каждый этап модифицируется: стены, например, можно возвести из дерева, кирпича или газобетона.

Простыми словами: Шаблонный метод определяет каркас выполнения определённого алгоритма, но реализацию самих этапов делегирует дочерним классам.

Обратимся к коду. Допустим, у нас есть программный инструмент, позволяющий тестировать, проводить контроль качества кода, выполнять сборку, генерировать отчёты сборки (отчёты о покрытии кода, о качестве кода и т. д.), а также развёртывать приложение на тестовом сервере.

Изначально у нас есть наш Builder, который описывает скелет для построения алгоритма:

abstract class Builder
{

    // Шаблонный метод
    final public function build()
    {
        $this->test();
        $this->lint();
        $this->assemble();
        $this->deploy();
    }

    abstract public function test();
    abstract public function lint();
    abstract public function assemble();
    abstract public function deploy();
}
Затем у нас есть его реализации:

class AndroidBuilder extends Builder
{
    public function test()
    {
        echo 'Запуск Android тестов';
    }

    public function lint()
    {
        echo 'Копирование Android кода';
    }

    public function assemble()
    {
        echo 'Android сборка';
    }

    public function deploy()
    {
        echo 'Развертывание сборки на сервере';
    }
}

class IosBuilder extends Builder
{
    public function test()
    {
        echo 'Запуск iOS тестов';
    }

    public function lint()
    {
        echo 'Копирование iOS кода';
    }

    public function assemble()
    {
        echo 'iOS сборка';
    }

    public function deploy()
    {
        echo 'Развертывание сборки на сервере';
    }
}
Пример использования:

$androidBuilder = new AndroidBuilder();
$androidBuilder->build();

// Вывод:
// Запуск Android тестов
// Копирование Android кода
// Android сборка
// Развертывание сборки на сервере

$iosBuilder = new IosBuilder();
$iosBuilder->build();

// Вывод:
// Запуск iOS тестов
// Копирование iOS кода
// iOS сборка
// Развертывание сборки на сервере

[содержание](/readme.md)  
