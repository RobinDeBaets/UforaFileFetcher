# UforaFileFetcher

A multithreaded Python tool to download files from [Ufora](https://ufora.ugent.be) (Brightspace) automatically using the BrightSpace API.
Supports 2FA .

Extra features:
- Create PDFs of file and module metadata (requires `wkhtmltopdf`)
- Automatically convert .ppt and .pptx files to .pdf (requires `unoconv`)

**LICENSE**: [WTFPL](https://en.wikipedia.org/wiki/WTFPL)

## Setup
 
```
sudo apt install wkhtmltopdf # Optional
sudo apt install unoconv # Optional
git clone https://github.com/RobinDeBaets/UforaFileFetcher
cd UforaFileFetcher
pip3 install .
```

You can now run the setup.
```
uforafilefetcher setup
```

![](images/setup.png)

### Development environment

```
python3 -m venv venv
source venv/bin/activate
pip install -e . 
```


## Usage

### Sync

Will sync the configured courses to the configured output directory as specified in the config file. This will ignore files that have already been downloaded.

```
uforafilefetcher sync <config>
```

![](images/sync.png)

Config files can be generated with `uforafilefetcher setup`, but can also be manually created following this layout:

```
{
    "output_directory": "~/university/ufora/",
    "courses": [
        438620,
        442195,
        438596,
        450000
    ],
    "credentials": {
        "email": "foo.bar@ugent.be",
        "password": "azerty123",
        "otc_secret": "pppmmmvvv"
    }
}

```


### List courses


```
uforafilefetcher courses <config>
```

### Download course

Will download a specific course to the specified output directory. Use the previous command to find out the id of your 
courses.

```
uforafilefetcher download <course_id> <config> [output_dir]
```

### Show help

```
uforafilefetcher help
```
