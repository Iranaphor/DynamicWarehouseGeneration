function tml () {
    whiptail_config $1
    export T="Select a .TMuLE File"

    #Select a TMuLE to load
    tmule_list=$(get_tmules)
    ans1=$(whiptail --title "$T" --notags --menu "TMuLE Files:" $WT_height $WT_width $WT_menu_height 3>&1 1>&2 2>&3 $tmule_list)
    if [[ $ans1 == "" ]] ; then
        whiptail --title "$T" --msgbox "No TMuLE Selected" $WT_height $WT_width $WT_menu_height 3>&1 1>&2 2>&3
        return
    fi

    #Select an action
    export file_end=${ans1##*'/tmule/'}
    export N=$(echo "launch" Launch "relaunch" Re-Launch "stop" Stop "terminate" Terminate)
    ans2=$(whiptail --title "$T" --notags --menu "Do what with $file_end?" $WT_height $WT_width $WT_menu_height 3>&1 1>&2 2>&3 $N)
    if [[ -z "$ans2" ]] ; then
        whiptail --title "$T" --msgbox "No Action Selected" $WT_height $WT_width $WT_menu_height 3>&1 1>&2 2>&3
        return
    fi

    #Perform file-specific actions
    tmule -c $ans1 $ans2
    return
}

function get_tmules () {
    #if empty run updatedb
    unset tmule_list
    for value in $(locate *.tmule | grep warez);
    do
        key=$value
        ref="${value##*/}"; ref="${ref%.*}"
        pkg="${value%%/tmule*}"; pkg="${pkg##*/}"

        tmule_list+="$key ($pkg)---$ref "
    done
    echo $tmule_list
}
