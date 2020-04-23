LINK_TEXT_SELF = 'a[text()]' # 自身がテキストを持つa
LINK_TEXT_CHILD = 'a[child::*/text()]' # 子要素がテキストを持つa
LINK_TEXT_RECURSIVE = 'a[//text()]' # 自身または子要素がテキストを持つa(再帰的)
LINK_IMAGE = 'a[//img]' # 画像リンクのa
TEXT_INPUT = 'input[@type="text"]'
PASSWORD_INPUT = 'input[@type="password"]'
INPUT_RADIO = 'input[@type="radio"]'
INPUT_CHECKBOX = 'input[@type="checkbox"]'
SELECT = 'select'
SELECT_OPTION = 'select//option'

WITH_LABEL = '[@id=ancestor::html//label/attribute::for]' # forでリンクしたlabelを持つinput
WITH_INPUT = '[@for=ancestor::html//input/attribute::id]' # forでリンクしたinputを持つlabel
WRAPPED_BY_LABEL = '[ancestor::label]' # labelに囲まれたinput
WRAPS_INPUT = '[child::input]' # inputを囲むlabel