BEGIN {
    print "#! /bin/bash"
    print "# Some conventions for errnos"
    print ""
}
/define.E/ {
    if ($3 ~ "[[:digit:]]+") {
        print "export " $2 "=" $3
    } else {
        print "export " $2 "=$" $3
    }
}

