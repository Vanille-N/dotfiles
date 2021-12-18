BEGIN {
    print "#! /bin/bash"
    print "# homebrewn perror"
    print ""
    print "if [[ $# != 1 ]]; then"
    print "  echo \"-- Usage: perror ERRNUM\" --"
    print "  exit $EINVAL"
    print "fi"
    print ""
    print "case $1 in"
    print "    (0) echo \"Success\";;"
}
/define.E/ {
    if ($3 ~ "[[:digit:]]+") {
        MSG = $5
        for (i = 6; i < NF; i++) {
            MSG = MSG " " $i
        }
        print "    (" $3 ") echo \"" MSG "\";;"

    }
}
END {
    print "    (*)"
    print "        echo \"-- No such error code --\""
    print "        exit $EINVAL"
    print "        ;;"
    print "esac"
}

