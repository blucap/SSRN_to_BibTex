# SSRN_to_BibTex

This command line-based python script returns a BibTex entry from the SSRN article id or the url. 

Copy the `ssrn.py` file to a location that your system's path can find, e.g.  `\usr\local\ssrn` 

Usage:

```
ssrn 2828073
```

or, using the full path from your browser:

```
ssrn https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2828073
```

which generates this output:  

    Risk Management, Governance, Culture, and Risk Taking in Banks
    
    Author's name:
    René M. Stulz (17753)
    
    Bibtex:
    
    @article{Stulz2016,
    author = {Stulz, René M.},
    title = {{Risk Management, Governance, Culture, and Risk Taking in Banks}},
    pages = {43-60},
    publisher = {Elsevier BV},
    note = "\url{https://ssrn.com/abstract=2828073}",
    month = sep,
    year = 2016
    }
    
    https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2828073

You can then copy and paste the text into your bib library file.

Now, don't panic if you get some error messages, as ssrn.com doesnt like scraping. Just try, using the number (`ssrn 2828073`)  or the url notation: `ssrn https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2828073`