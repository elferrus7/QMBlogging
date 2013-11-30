<?php

//phpinfo();
//$response =file_get_contents("https://www.googleapis.com/freebase/v1/search?query=morelos&indent=true&lang=es"); //http_get("https://www.googleapis.com/freebase/v1/search?query=morelos&indent=true&lang=es", array("timeout"=>1), $info);
//print_r($response);

/*
//$curl = curl_init('https://www.googleapis.com/freebase/v1/search?query=morelos&indent=true&lang=es'); 
$curl = curl_init('https://www.googleapis.com/freebase/v1/search?query=Secretaría_de_Gobernación&indent=true&lang=es'); 
curl_setopt($curl, CURLOPT_FAILONERROR, true); 
curl_setopt($curl, CURLOPT_FOLLOWLOCATION, true); 
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true); 
curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false); 
curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);   
$result = curl_exec($curl); 
echo $result;
echo "<br><br><br>";
$resDecode = json_decode($result);
//var_dump(json_decode($result));

    //$r = $resDecode->{'result'};
//$r2 = $r->{'notable'};
$t = $resDecode->{"result"}[0]->{"notable"}->{"id"};
$tema = explode("/", $t);
    //print_r( $resDecode->{"result"}[0]->{"notable"}->{"id"} );
echo $tema[0];

//var_dump( $resDecode["result"]["name"] );
//echo $r2->{'name'};
//var_dump( $r);
*/

if( isset($_POST['enviar']) ){
    
    //$text = utf8_decode($_POST['text']);
    $text = $_POST['text'];
    
    echo 'Codificacion de '.$text.': '.mb_detect_encoding($text).'<br>';
    //echo 'Texto convertido UTF-8: '.  utf8_decode (mb_convert_encoding($text, "UTF-8", "auto") ).'<br>';
    
    echo $text.' -> ';
    $text = quitarAcentos( $text );
    echo $text.' <br>';
    
    /*$originales = 'ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞ
ßàáâãäåæçèéêëìíîïðñòóôõöøùúûýýþÿŔŕ';
    echo "COD caracteres: ".mb_detect_encoding($originales).'<br>';
    echo utf8_decode($originales).'<br>';
    echo "COD caracteres: ".mb_detect_encoding( utf8_decode($originales) ).'<br>';*/
    
    $text = str_replace(" ", "_", $text);
    $text = strtolower($text);
    
    //$rdf = 'https://www.googleapis.com/freebase/v1/text/en/'.$text.'?lang=es&format=html';
    $rdf = 'https://www.googleapis.com/freebase/v1/search?query='.utf8_encode($text).'&indent=true&lang=es';
                //echo utf8_encode($rfd);
    echo $rdf;
    $curl = curl_init($rdf); 
    curl_setopt($curl, CURLOPT_FAILONERROR, true); 
    curl_setopt($curl, CURLOPT_FOLLOWLOCATION, true); 
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true); 
    curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false); 
    curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);   
    $result = curl_exec($curl); 
    $resDecode = json_decode($result);
    
    for($i=0; $i<5; $i++){
        $t = $resDecode->{"result"}[$i]->{"notable"}->{"name"};
        //var_dump( $t );
        echo '<br> '.utf8_decode($t);
    }
    

}

function quitarAcentos ($cadena){
    /*$originales = 'ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõöøùúûýýþÿŔŕ';
     $modificadas = 'aaaaaaaceeeeiiiidnoooooouuuuybsaaaaaaaceeeeiiiidnoooooouuuyybyRr';*/
    //$originales = '';
    //echo '<br>'.$originales.'<br>';
    
    /*$originales = utf8_decode($originales);
    $cadena = strtr($cadena, $originales, $modificadas);
    $cadena = strtolower($cadena);
    return $cadena;*/
    
    /*$tofind = "ÀÁÂÄÅàáâäÒÓÔÖòóôöÈÉÊËèéêëÇçÌÍÎÏìíîïÙÚÛÜùúûüÿÑñ";
    $replac = "AAAAAaaaaOOOOooooEEEEeeeeCcIIIIiiiiUUUUuuuuyNn";
    //return utf8_encode(strtr(utf8_decode($cadena), utf8_decode($tofind), $replac)); 
    return strtr(utf8_decode($cadena), utf8_decode($tofind), $replac);*/
    
    $tofind = "ÁáÉéÍíÓóÚúÑñ";
    $replac = "AaEeIiOoUuNn";
    //return utf8_encode(strtr(utf8_decode($cadena), utf8_decode($tofind), $replac)); 
    return strtr($cadena, $tofind, $replac); 
    
}

?>
<form method="post" action="pruebaPeticion.php">
    <input name="text" type="text" />
    <input type="submit" value="Enviar" name="enviar" />
</form>