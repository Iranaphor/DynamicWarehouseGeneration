function whiptail_config () {

    export PRIMARY=white
    export SECONDARY=gray
    export default="color12"
    export ACCENT="${1:-$default}"

    export NEWT_COLORS="
        root=,$SECONDARY;
        border=$PRIMARY,$ACCENT;
        window=,$PRIMARY;

        title=$PRIMARY,$ACCENT;

        entry=$SECONDARY,$PRIMARY;
        textbox=$ACCENT,$PRIMARY;
        acttextbox=$PRIMARY,$SECONDARY;

        listbox=$ACCENT,$PRIMARY;
        actlistbox=$PRIMARY,$SECONDARY;
        sellistbox=$PRIMARY,$SECONDARY;
        actsellistbox=$PRIMARY,$ACCENT;

        button=$PRIMARY,$ACCENT;
        actbutton=$PRIMARY,$SECONDARY;
        compactbutton=$PRIMARY,$SECONDARY;
    "

    high=55
    rows=$(stty size | cut -d' ' -f1)
    [ -z "$rows" ] && rows=$high
    [ $rows -gt $high ] && rows=$high
    cols=$(stty size | cut -d' ' -f2)
    export WT_height=$rows
    export WT_width=$((cols - 10))
    export WT_menu_height=$((rows-10))
}
