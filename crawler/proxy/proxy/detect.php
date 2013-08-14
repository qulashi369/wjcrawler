<?php

    echo "PROXYDETECTATION</br>";
    echo "REMOTE_ADDR</br>";
    var_dump($_SERVER['REMOTE_ADDR']);
    echo "</br>";
    echo "env_REMOTE_ADDR</br>";
    var_dump(getenv('REMOTE_ADDR'));
    echo "</br>";
    echo "env_HTTP_CLIENT_IP</br>";
    var_dump(getenv('HTTP_CLIENT_IP'));
    echo "</br>";
    echo "HTTP_CLIENT_IP</br>";
    var_dump($_SERVER['HTTP_CLIENT_IP']);
    echo "</br>";
    echo "HTTP_X_FORWARDED_FOR</br>";
    var_dump($_SERVER['HTTP_X_FORWARDED_FOR']);
    echo "</br>";
    echo "HTTP_X_FORWARDED</br>";
    var_dump($_SERVER['HTTP_X_FORWARDED']);
    echo "</br>";
    echo "HTTP_X_CLUSTER_CLIENT_IP</br>";
    var_dump($_SERVER['HTTP_X_CLUSTER_CLIENT_IP']);
    echo "</br>";
    echo "HTTP_FORWARDED_FOR</br>";
    var_dump($_SERVER['HTTP_FORWARDED_FOR']);
    echo "</br>";
    echo "HTTP_FORWARDED</br>";
    var_dump($_SERVER['HTTP_FORWARDED']);
    echo "</br>";

?>
