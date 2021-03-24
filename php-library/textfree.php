<?php
require 'uuid.php';

function makeaccount() {
    $udid1 = UUID::makeudid();
    $udid2 = UUID::makeudid();
    $udidending = uniqid();
    $pin = rand(1111111111,9999999999);
    $data = array(
        "accountType"=> "email",
        "clientId"=> "textfree-android-$udid1-$udidending",
        "device"=> "unknown",
        "email"=> "$udid1@ligma.vip",
        "installationId"=> "$udid1-$udidending",
        "marketingId"=> "9022041723545822",
        "notificationTokenInfo"=> array(
            "notificationStatus"=> 1,
	    // this access token doesnt matter its only for getting notifications on android.
            "notificationToken"=> "cyO-8P50y8M:APA91bFhYNFCwG6bvp37GKTyPDZ1f5NpJ8hbDfaE_ddkvJRAXQsTBOIiwI26sLLJ402yQ4g2bjGhd-aAlN54womXnk3b7tPXG9L0ppOJ_9rziuA5zuzUefO13jxvft7Gsoe94j9C_p-a",
            "notificationType"=> "G"
        ),
        "password"=> $udidending,
        "pin"=> $pin,
        "systemProperties"=>array(
            "board"=> "unknown",
            "bootloader"=> "uboot",
            "brand"=> "unknown",
            "cpu-abi"=> "armeabi-v7a",
            "cpu-abi2"=> "armeabi",
            "device"=> "unknown",
            "device-id"=> $udid1,
            "display"=> "-user 5.1.1 20171130.276299 release-keys",
            "fingerprint"=> "//:5.1.1/20171130.376229:user/release-keys",
            "google.account"=> "dontworryaboutmyaccount@yourbad.com",
            "hardware"=> "intel",
            "host"=> "se.infra",
            "http.agent"=> "Dalvik/2.1.0 (Linux; U; Android 5.1.1; unknown Build/LMY48Z)",
            "http.keepAlive"=> "false",
            "http.nonProxyHosts"=> "",
            "http.proxyHost"=> "192.168.1.14",
            "http.proxyPort"=> "8080",
            "https.nonProxyHosts"=> "",
            "https.proxyHost"=> "192.168.1.14",
            "https.proxyPort"=> "8080",
            "id"=> "LMY48Z",
            "java.io.tmpdir"=> "/data/data/com.pinger.textfree/cache",
            "mac"=> "30:4d:66:3e:51:a5",
            "manufacturer"=> "unknown",
            "model"=> "unknown",
            "product"=> "unknown",
            "radio"=> "unknown",
            "tags"=> "release-keys",
            "type"=> "user",
            "unknown"=> "unknown",
            "user"=> "unknown",
            "user.home"=> "",
            "version.codename"=> "REL",
            "version.incremental"=> "eng.se.infra.20190315.173723",
            "version.release"=> "5.1.1",
            "version.sdk"=> "22",
            "version.sdk-int"=> "22"
        ),
        "timezone"=> array(
            "januaryOffset"=> 480,
            "julyOffset"=> 480
        ),
        "udid"=> $udid1,
        "version"=> "8.37.2",
        "versionOS"=> "5.1.1"
    );

    $ch = curl_init("https://api.pinger.com/1.0/account/registerWithLang?lang=en_US&cc=US");
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");
    //send this via tor.
    curl_setopt($ch, CURLOPT_PROXY, "socks5://localhost:9050");
    curl_setopt($ch, CURLOPT_PROXYTYPE, CURLPROXY_SOCKS5);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    //headers
    curl_setopt($ch, CURLOPT_HTTPHEADER, array(
        "x-rest-method: POST",
        "Content-Type: application/json",
        "X-Install-Id: 9dc84cf2e7f74bfb227112e585bb6a08",
        "x-client: textfree-android,8.37.2,177_RC_v.37.2_STORE_CONFIG",
        "x-os: android,5.1.1",
        "x-gid: 48",
        "x-udid: $udid1,$udid2",
        "Authorization: OAuth realm=\"https://api.pinger.com\", oauth_consumer_key=\"textfree-android\", oauth_signature_method=\"HMAC-SHA1\", oauth_timestamp=\"1554164172\", oauth_nonce=\"hroswbaqylsmoana\", oauth_signature=\"LwylVD71c9rrtzqO1CH86A01yq4%3D\"",
        "Host: api.pinger.com",
        "User-Agent: okhttp/3.11.0"
    ));
    $res = json_decode(curl_exec($ch), true);
    curl_close($ch);
    $result = array(
        "username" => "$udid1@ligma.vip",
        "password" => $udidending,
        "userId" => $res["result"]["userId"],
        "udid_1" => $udid1,
        "udid_2" => $udid2,
        "pin" => $pin
    );
    return $result;
}


function get_numbers($areaCode, $udid1, $udid2) {
    $ch = curl_init("https://api.pinger.com/1.0/account/phone/listAvailableDnxNumbers");
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "POST");
    curl_setopt($ch, CURLOPT_PROXY, "socks5://localhost:9050");
    curl_setopt($ch, CURLOPT_PROXYTYPE, CURLPROXY_SOCKS5);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true); 
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode(array("areaCode"=>$areaCode)));
    curl_setopt($ch, CURLOPT_HTTPHEADER, array(
        "x-rest-method: GET",
        "Content-Type: application/json",
        "X-Install-Id: 9dc84cf2e7f74bfb227112e585bb6a08",
        "x-client: textfree-android,8.37.2,177_RC_v.37.2_STORE_CONFIG",
        "x-os: android,5.1.1",
        "x-gid: 48",
        "x-udid: $udid1,$udid2",
        "Authorization: OAuth realm=\"https://api.pinger.com\", oauth_consumer_key=\"textfree-android\", oauth_signature_method=\"HMAC-SHA1\", oauth_timestamp=\"1554168144\", oauth_nonce=\"olfrwkveeoyyvooy\", oauth_signature=\"ChiA%2BxB95l%2FswoI%2FgVG48r%2FH%2Fbw%3D\"",
        "Host: api.pinger.com",
        "User-Agent: okhttp/3.11.0"
    ));
    $res = curl_exec($ch);
    curl_close($ch);
    return $res;
}


?>
