Instructions how to generate CADI sheets:

```
> git clone git@github.com:cmsdoxy/tools.git

> cd tools/sheets
```
Follow [1] instruction if you have updated list of USA LPC authors 
```
> chmod +x generate_sheets.sh && ./generate_sheets.sh
```


You will be asked to enter your login and password, because CADI requires authentication in order to acces data.

...wait... take a break :)

Generated sheets will be stored in **sheets** directory as csv files. Separator is pipe `|`

For the first time script will take about 30mins because it downloads a lot of data from CADI.

In case of error:

1. launch `chmod +x cleanup.sh && ./cleanup.sh`

2. try again `./generate_sheets.sh`

3. if problem persists contact `mantas.stankevicius@cern.ch` until Nov 30 2013. After this date contact `ali.mehmet.altundag@cern.ch`


---

**[1] Instuction**

1.Convert updated_list_of_authors.xls(x) to **usa_lpc_authors.csv**

**IMPORTANT!**

Do not mistype filename **usa_lpc_authors.csv**

Field delimiter - **|**

Text delimiter - None (leave empty field)

2.Replace existing **usa_lpc_authors.csv** with new one in **data** directory.

---

