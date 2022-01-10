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



**Mosaic Application Command**

> 
> 
> **Mosaic App:**
> 
> > *Mosaic Application*
> > 
> > **Call Command :** `None` Default Running Mosaic App.
> > 
> > 
> > 
> > **--template :** Set Templates Path or Name if in `Default Templates Dir` For `encrypt/mosaic` or `decrypt/data` - default is `config[default]`.
> > 
> > 
> > 
> > **--mode :** Set Action Mode `mosaic/enc` or `data/dec` - default is `enc`
> > 
> > 
> > 
> > **--text :** Text Data For `encrypt/mosaic` or `decrypt/data`.
> > 
> > 
> > 
> > **--file :** File Data For `encrypt/mosaic` or `decrypt/data`.
> > 
> > 
> > 
> > **--res :** Set Result File Path For Saving Result Optional If Input is `--text` - default is `None`.
> > 
> > 
> > 
> > **--startblock :** Set Start Block `reletive start block` - default is `0`
> 
> 
> 
> **Template App:**
> 
> > *Generate New Template*
> > 
> > **Call Command :** `template, *tt`
> > 
> > 
> > 
> > **file :** File Path Or Templates Name if Want Save To `Default Templates Dir`
> > 
> > 
> > 
> > **--replace :** Force Write If Exists Template File.
> > 
> > 
> > 
> > **--order :** Make Templates Order - Use `'-'` For Templates Generate Order.
> > 
> > 
> > 
> > **--string :** Make Order From StringPassword.
> > 
> > 
> > 
> > **--length :** Options If Use `--string` Options For Making Custom Length Order From String Password. default Use String `Length`.
> > 
> > 
> > 
> > **--repeat :** Repeat Order For Make Templates. default is `1`.
> > 
> > 
> > 
> > **--size :** For Making Templates With How Many Blocks If Order is `None` And Use Not `--string`.
> > 
> > **--saveorder :** Saving Order To OrderStore. default is `False`.
> > 
> > 
> 
> 
> 
> **Manage App:**
> 
> > *Manage Mosaic App*
> > 
> > **Call Command :** `manage, *ma`
> > 
> > 
> > 
> > **--makefromfile :** Make Templates From File Need To Value First OrderFile Path Second is Directory Path For Use Default Templates Dir use Empty string.
> > 
> > 
> > 
> > **--updateconf :** Update Config File With Other Config File.
> > 
> > 
> > 
> > **--conf :** Show Config File Path.
> > 
> > 
> > 
> > **--templates :** Show Default Templates Dir Path.
> > 
> > 
> > 
> > **--templatelist :** Show All Templates Name in Default Templates Dir.
> > 
> > 
> > 
> > **--resetconf :** Reset Config File To Default.
> > 
> > 
> > 
> > **--resettemplates :** Reset Templates Default Dir - Delete All Templates File and Order Store Then Generate Default Template Only.




