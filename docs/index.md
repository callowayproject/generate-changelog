# Generate Changelog

{% 
    include-markdown 
    "../README.md" 
    start="<!--start-->" 
    end="<!--end-->"
    rewrite-relative-urls=false
%}
