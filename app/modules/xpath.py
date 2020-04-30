class Xpath:
  """nodes"""
  textLink = 'a[text()]'
  imageLink = 'a[/img]'
  formText = 'input[@type="text"]'
  formPassword = 'input[@type="password"]'
  formRadio = 'input[@type="radio"]'
  formCheckbox = 'input[@type="checkbox"]'
  formSelect = 'select'

  """options"""
  def getOptionByPairInput(node: str):
    # labelノードから対応するinputを探すためのオプションを返す
    return '[@id=ancestor::html//%s/attribute::for]' % node
  def getOptionByPairLabel(node: str):
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
    optionFor = '@for=ancestor::html//%s/attribute::id' % (node)
    optionWrap = 'descendant::%s' % (node)
    return 'label[%s or %s]' % (optionFor, optionWrap)

  def getInputbyLabel(node: str):
    # 引数のlaeblノードに対応するinputのノード
    optionFor = '@id=ancestor::html//%s/attribute::for' % (node)
    optionWrap = 'ancestor::%s' % (node)
    return 'Input[%s or %s]' % (optionFor, optionWrap)