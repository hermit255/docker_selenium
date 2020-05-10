class Xpath:
  """nodes"""
  textLink = 'a[text()]'
  imageLink = 'img[ancestor::a]'
  formText = 'input[@type="text"]'
  formPassword = 'input[@type="password"]'
  formRadio = 'input[@type="radio"]'
  formCheckbox = 'input[@type="checkbox"]'
  formSelect = 'select'

  """options"""
  def getOptionByPairLabel(node: str):
    # labelノードから対応するinputを探すためのオプションを返す
    return '[@id=ancestor::html//%s/attribute::for]' % node
  def getOptionByPairInput(node: str):
    # inputノードから対応するlabelを探すためのオプションを返す
    return '[@for=ancestor::html//%s/attribute::id]' % node
  def getOptionByWrappingLabel(node: str):
    # 囲んでいるlabelノードからinputを探すためのオプションを返す
    return '[ancestor::%s]' % node
  def getOptionByWrappedInput(node: str):
    # 囲まれているinputノードからinputを探すためのオプションを返す
    return '[descendant::%s]' % node

  def getLabelbyInput(node: str):
    # 引数のinputノードに対応するlabelのノード
    # inputノードを特定しなければ、対応するinputを持つlabelノードを探せる
    optionFor = '@for=ancestor::html//%s/attribute::id' % (node)
    optionWrap = 'descendant::%s' % (node)
    return 'label[%s or %s]' % (optionFor, optionWrap)

  def getInputbyLabel(node: str):
    # 引数のlaeblノードに対応するinputのノード
    # labelノードを特定しなければ、対応するlabelを持つinputノードを探せる
    optionFor = '@id=ancestor::body//%s/attribute::for' % (node)
    optionWrap = 'ancestor::%s' % (node)
    return 'Input[%s or %s]' % (optionFor, optionWrap)

  def getImgByElement(element):
    text = element.text
    href = element.get_attribute('href') or ''
    return f'img[ancestor::a[text()="{text}" and @href="{href}"]]'

  def getLabelByElement(element):
    id = element.get_attribute('id') or ''
    name = element.get_attribute('name') or ''
    value = element.get_attribute('value') or ''

    return f'{optionFor}|{optionWrap}'
    optionFor = f'@for={id}'
    optionWrap = 'descendant::input[@name="{name}" and @value="{value}"]'
    return 'label[{optionFor} or {optionWrap}]'
