## Комментарии к заданию 2

**Текст:** Роман _"Ĉu vi kuiras ĉine?"_, автор Клод Пирон, Claude Piron (под псевдонимом Йоган Валано, Johán Valano)

**Язык:** эсперанто

### Предобработка текста
- В эсперанто можно сокращать некоторые слова апострофом, в т.ч. существительные:
  - ...o → ...' (им. сущ. в им. п. ед. ч.)

  Однако такие сокращения используются в основном в поэзии
- Кроме того, Клод Пирон придумывает диалект региону, в котором происходит часть действия романа. Говорящим на этом диалекте свойствено, среди прочего
  - применять вышеупомянутое сокращение чаще обыкновенного
  - вместо апострофа помечать это сокращение акутом (ˊ), например doktor' → doktór
- Также в тексте персонажей часто называют по фамилии, и отличить мужа и жену возможно лишь по наличию титулов s-ro (sinjoro), s-ino (sinjorino), d-ro (doktoro), f-ino (fraŭlino), ges-roj (gesinjoroj)

Это всё необходимо иметь в виду во время работы с текстом

### Список персонажей
Для конструирования списка я извлёк все имена собственные (слова с большой буквы не в начале предложения) при помощи name_extractor.py и вручную исправил его. В итоге получился файл, где в каждой строке были написаны все имена одного персонажа, а также помечен пол при необходимости

### Анализ связей
Так как я лентяй и взялся за дз поздно, времени на анализ диалогов у меня не хватило. Поэтому в analyzer.py код лишь подсчитывает, насколько часто имена персонажей оказываются близко друг к другу.

В файле `grafo.png` представлен граф, получающийся в Gephi после такого анализа.

Ожидаемо, среди людей с наибольшим числом связей главный герой Яно Караль, его жена Джойя Караль, а также Пауло Йорли - мужчина, чью смерть расследует Яно в книге. Забавно так же, как много связей набралось у Марты Боломай, последнего опрашиваемого в списке - она очень болтлива. В одном монологе она много раз упомянула несколько людей, которые больше нигде в романе не встречались, и в итоге они образовали своё отдельное облачко
