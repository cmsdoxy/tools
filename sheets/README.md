Instructions how to generate CADI sheets:

```
> git clone git@github.com:cmsdoxy/tools.git

> cd tools/sheets

> chmod +x generate_sheets.sh && ./generate_sheets.sh
```

You will be asked to enter your login and password, because CADI requires authentication in order to acces data.

...wait... take a break :)

For the first time script will take about 30mins because it downloads a lot of data from CADI.

In case of error:

1. delete **data** and **sheets** directories `rm -R data sheets`

2. try again `./generate_sheets.sh`

3. if problem persists contact `mantas.stankevicius@cern.ch` until Nov 30 2013. After this date contact `ali.mehmet.altundag@cern.ch`


