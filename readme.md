# UforaFileFetcher

A simple tool to download files from Ufora (Brightspace) automatically using the BrightSpace API.
The tool can download files and create PDF summaries of metadata of files and modules.

For fun purposes **ONLY**.

## Setup
 
### Dependencies

```
sudo apt install python3-venv
sudo apt install wkhtmltopdf
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Credentials

This tool will need your credentials. These can be configured once and will be saved to `credentials.json` in plaintext, due to a lack of a better alternative.

```
./uforafilefetcher setup
```

## Usage

### List courses

```
./uforafilefetcher courses

Output:
 ID        NAME
  53989    C003785A - Automaten, berekenbaarheid en complexiteit
  55203    C003806A - Inleiding tot de elektrotechniek
  56798    C003783A - Logisch programmeren
  58257    C003784A - Software Engineering Lab 2
  61295    C003789A - Computationele biologie
```

### Download files

```
./uforafilefetcher download <course_id> <output_dir>

> ./uforafilefetcher download 56798
Output:
Downloading Hoofdstuk 1.pdf: 1.95MB [00:02, 844kB/s]                                                                                                                                                                                                     
Downloading Gebruikte Boeken.html: [00:00<00:00, 25.2kB/s]
Creating metadata Gebruikte Boeken.pdf
Downloading 10_zebra.pl: 3.07kB [00:00, 43.3kB/s]                                                                                                                                                                                                        
Downloading 9_exists.pl: 1.02kB [00:00, 4.43kB/s]                                                                                                                                                                                                        
Downloading 8_may_steal.pl: 1.02kB [00:00, 14.9kB/s]                                                                                                                                                                                                     
Downloading 7_sister_of.pl: 1.02kB [00:00, 13.5kB/s]                                                                                                                                                                                                     
Downloading 6_likes.pl: 1.02kB [00:00, 14.4kB/s]                                                                                                                                                                                                         
Downloading 5_likes.pl: 1.02kB [00:00, 14.6kB/s]                                                                                                                                                                                                         
Downloading 4_likes.pl: 1.02kB [00:00, 6.04kB/s]                                                                                                                                                                                                         
Downloading 3_feiten.pl: 1.02kB [00:00, 16.7kB/s]                                                                                                                                                                                                        
Downloading 2_feiten.pl: 1.02kB [00:00, 2.62kB/s]                                                                                                                                                                                                        
Downloading 1_likes.pl: 1.02kB [00:00, 14.5kB/s]                                                                                                                                                                                                         
Creating metadata Oefeningen Dodona.pdf

File structure:
Logisch Programmeren
├── Boeken
│   ├── Gebruikte Boeken.html
│   └── Gebruikte Boeken.pdf
├── Code
│   └── HOC 1
│       ├── 10_zebra.pl
│       ├── 1_likes.pl
│       ├── 2_feiten.pl
│       ├── 3_feiten.pl
│       ├── 4_likes.pl
│       ├── 5_likes.pl
│       ├── 6_likes.pl
│       ├── 7_sister_of.pl
│       ├── 8_may_steal.pl
│       └── 9_exists.pl
├── Oefeningen
│   └── Oefeningen Dodona.pdf
└── Slides
    └── Hoofdstuk 1.pdf
```

### Sync

Configure `config.json` to contain the courses that you want to sync
```
> nano config.json
{
  "output_directory": "~/university/ufora",
  "courses": [
    53989,
    55203,
    56798,
    58257,
    61295
  ]
}

```
Run tool
```
./uforafilefetcher sync
```