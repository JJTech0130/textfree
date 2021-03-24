<?php
require 'textfree.php';
function main() {
    if(!isset($_GET['areaCode']))
        echo "please pass areaCode=[area code]";
    else if(!isset($_GET["udid1"]))
        echo "please pass your udid1: udid1=[your udid1]";
    else if(!isset($_GET["udid2"]))
        echo "please pass your udid2: udid2=[your udid2]";
    else
        echo get_numbers($_GET['areaCode'], $_GET["udid1"], $_GET["udid1"]);
}
main()
?>
