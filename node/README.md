###Init

First run:
```
npm install
```

Add file named /config.json in this structure:
```
[
    {
        "url": "https://example.com",
        "selector":"ANY_VALID_SELECTOR",
        "interval": 10,//in minutes, not seconds
        "fileName": "THE_FILE_NAME_TO_SAVE_AS"
    },{
        "url": "https://example2.com",
        "selector":"ANY_VALID_SELECTOR2",
        "interval": 2000,//in minutes, not seconds
        "fileName": "THE_FILE_NAME_TO_SAVE_AS2"
    }
]
```

###Run
```
node index.js
```