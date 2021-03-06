##### IN THE NAME OF GOD

# MOSAICI

---

*SHORT :*

> Protocol For Make Secure Data Use Template .
> 
> This Method Use Index Of Value in Current Block And Secure Input Data With.
> 
> With Out `XOR`, `AND`, `OR` Method . This Protocol Create New Data With Indexes Of Source Value.
> 
> **Result :** Make New Data With Indexes Of Value In Blocks Of Template.
> 
> *NOTE :* To `decode/data` Data, must have the Template used to `encrypt/mosaic` or the PasswordString or Template Order to create the Right Template.



Create Template with Blocks Each Block Use `default = 256` Array Members Of Bytes `0, 255` Each Template Use Multi Block . Secure Data Use Index Of Data in Template Current Block .

This Protocol Make New Data With Indexes Of Value So Your Data Not Exists in The New Data Only Index of Value From Current Block in Templates Exists So Secure :).



`Install Mosaici Protocol`

```bash
pip install mosaici
```



`Use Mosaic App`

```bash
python -m mosaici --text "test"
--
041D537C
--
python -m mosaici --text "041D537C" --mode dec
```



**Mosaic Application Command**

> **Mosaic App:**
> 
> > *Mosaic Application*
> > 
> > **Call Command :** `None` Default Running Mosaic App.
> > 
> > **--template :** Set Templates Path or Name if in `Default Templates Dir` For `encrypt/mosaic` or `decrypt/data` - default is `config[default]`.
> > 
> > **--mode :** Set Action Mode `mosaic/enc` or `data/dec` - default is `enc`
> > 
> > **--text :** Text Data For `encrypt/mosaic` or `decrypt/data`.
> > 
> > **--file :** File Data For `encrypt/mosaic` or `decrypt/data`.
> > 
> > **--res :** Set Result File Path For Saving Result Optional If Input is `--text` - default is `None`.
> > 
> > **--startblock :** Set Start Block `reletive start block` - default is `0`
> 
> **Template App:**
> 
> > *Generate New Template*
> > 
> > **Call Command :** `template, *tt`
> > 
> > **file :** File Path Or Templates Name if Want Save To `Default Templates Dir`
> > 
> > **--replace :** Force Write If Exists Template File.
> > 
> > **--order :** Make Templates Order - Use `'-'` For Templates Generate Order.
> > 
> > **--string :** Make Order From StringPassword.
> > 
> > **--length :** Options If Use `--string` Options For Making Custom Length Order From String Password. default Use String `Length`.
> > 
> > **--repeat :** Repeat Order For Make Templates. default is `1`.
> > 
> > **--size :** For Making Templates With How Many Blocks If Order is `None` And Use Not `--string`.
> > 
> > **--saveorder :** Saving Order To OrderStore. default is `False`.
> 
> **Manage App:**
> 
> > *Manage Mosaic App*
> > 
> > **Call Command :** `manage, *ma`
> > 
> > **--makefromfile :** Make Templates From File Need To Value First OrderFile Path Second is Directory Path For Use Default Templates Dir use Empty string.
> > 
> > **--updateconf :** Update Config File With Other Config File.
> > 
> > **--conf :** Show Config File Path.
> > 
> > **--templates :** Show Default Templates Dir Path.
> > 
> > **--templatelist :** Show All Templates Name in Default Templates Dir.
> > 
> > **--resetconf :** Reset Config File To Default.
> > 
> > **--resettemplates :** Reset Templates Default Dir - Delete All Templates File and Order Store Then Generate Default Template Only.



#### Order :

*Order is a Pattern For Making Special Template Order*

**Order Syntax** is a Sequence of `HEX` Value With Mixer & Separator.

```python
# Order String
order = '54/72 65/68 64/69 72/73 20/4F 20/49 73/73 20/49 20/4F 72/73 64/69 65/68 54/72'
# '/' Mixer, ' ' Separator
# '54/72 ...' `54` Start Value, `72` End Value
```

**Order Object** instance of `BaseOrder` Ordet is Itarator Object

```python
# Import Order Object
from mosaici.order import Order

order_pattern = "54/72 65/68 64/69 ..."
order = Order(order_pattern)
# Or Can Use With Statement
with Order(order_pattern) as od:
    # Iterator Return Tuple[int, int]
    for start, end in od:
        # do stuff
```

Can Use `order_from_string` function. `support utf-8`

*arguments : (inp: str, length: int = None, separator: str= ' ', mixer: str = '/')*

```python
# Import order_from_string
from mosaici.order import order_from_string

text = "This Is Order"
# Generate Order Syntax From String
# arguments : (inp: str, length: int, separator: ' ', mixer: '/')
txt_to_order = order_from_string(text)
print(type(txt_to_order))
# `str`
print(txt_to_order)
# '54/72 65/68 64/69 72/73 20/4F 20/49 73/73 20/49 20/4F 72/73 64/69 65/68 54/72'
```

Or in Order Object Use `from_string` Static Method for Generating Order from String.

```python
# Import Order
from mosaici.order import Order

text = "This Is Order"
# Generate Order Syntax From String
# arguments : (inp: str, length: int, separator: ' ', mixer: '/')
txt_to_order = Order.from_string(txt)
print(type(txt_to_order))
# `str`
print(txt_to_order)
# '54/72 65/68 64/69 72/73 20/4F 20/49 73/73 20/49 20/4F 72/73 64/69 65/68 54/72'
```

arguments :

> Input : String input For Generating Order From that
> 
> Length : Make Order With Custom Length. default is None means Create Order With input length
> 
> Separator : Separator Symbol Use Order Object
> 
> Mixer : Mixer Symbol Use Order Object



#### Mosaic:

*Mosaic Object For Making Mosaici `encode`, and Data `decode`*

```python
# Import MosaicObject and MosaicMulti
from mosaici.mosaic import (
                MosaicObject,
                MosaicMulti,
                MosaicFile,
                MosaicMultiFile
                )
```

Use Mosaic Objects - `MosaicObject`, `MosaicMulti`, `MosaicFile`, `MosaicMultiFile` For Secure Data With Mosaici Protocol.

Mosaic Objects Support `with` Statements & Recomended For Use.

*NOTE : If Not Use with `with` statements & Use `FileTemplate` Must Manualy Closed After Done Working*

**Mosaici Multi Objects**  `MosaicMulti, MosaicMultiFile` Can Handle MultiTemplate for Working.

All Musaici Objects has 4 Method Septial Method -

`data_to_idx` for making indexes from data??. RETURN `GENERATOR` OBJECT

`idx_to_data` for making data from indexes input . RETURN `GENERATOR` OBJECT

`to_mosaic` like data_to_idx - some changes . RETURN `StoreFileIndexes` Object

`to_data` like idx_to_data - some changes. RETURN `ITERABLE` OBJECT

**Mosaic File Objects** Customize `to_mosaic`, `to_data` Methods For Working Better & Easy With File Input - in This Objects `to_mosaic` Auto Make New File For Result With inputing result Path. and `to_data` Method Auto Make New File With Res Path Input.

```python
# Import order_from_string, MosaicFile
from mosaici.order import order_from_string
from mosaici.mosaic import MosaicFile

order_str = order_from_string("This Is Order")

# Make Template From Order Then Create Indexes File or Data File
with MosaicFile(order=order_str) as mf:
    mosaic = mf.to_mosaic('./image.jpg', './ms_img.idx')
    # mosaic = mf.to_mosaic('./image.jpg', './ms_img.idx', start_block=10)
    data =  mf.to_data('./ms_img.idx', './image_back.jpg')
    # data =  mf.to_data('./ms_img.idx', './image_back.jpg', start_block=10)


# Use FileTemplate Very Faster - `Recomended`
template_file = ("./tmpl.tt", 256) # PATH, MEMBER
with MosaicFile(template_file) as mf:
    mosaic = mf.to_mosaic('./image.jpg', './ms_img.idx')
    # mosaic = mf.to_mosaic('./image.jpg', './ms_img.idx', start_block=10)
    data =  mf.to_data('./ms_img.idx', './image_back.jpg')
    # data =  mf.to_data('./ms_img.idx', './image_back.jpg', start_block=10)
```

and Use MosaicMulti Objects

```python
# Import Template, MosaicMultiFile
from mosaici.template import Template
from mosaici.mosaic import MosaicMultiFile

templates = {'tmp_1': Template(order=...), 'tmp_2': ('./tmpl.tt', 256)}

with MosaicMultiFile(templates) as mmf:
    mosaic = mmf.to_mosaic('./image.jpg', './ms_img.idx', 0, 'tmp_1')
    # make default template `mmf.template = 'tmp_1'`
    # mosaic = mmf.to_mosaic('./image.jpg', './ms_img.idx')
    data = mmf.to_data('./ms_img.idx', './image_back.jpg', 0, 'tmp_1')
    # data = mmf.to_data('./ms_img.idx', './image_back.jpg')
```



More info See Source.
