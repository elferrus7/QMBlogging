<?php
/*
 *  1- Obtener los tweets
 *  2- Analizar morfologicamente los tweets
 *  3- Filtrar las entidades que se van a consultar
 *  4- Consultar las entidades
 *  5- Guardar resultados
 * */
include ("analyzer.php");

class Freeling {
	// Adjust this path to your local FreeLing installation
	var $FL_DIR = "/usr";
	var $a;
	//Analiyzer
	var $m;
	//Mongo client
	var $db;
	//Database
	//Currente database
	var $tweets;
	var $entities;
	var $e_info;

	public function __construct() {
		//Launch Analizer
		$this -> a = new analyzer("8080", "-f $this->FL_DIR/share/freeling/config/en.cfg", "$this->FL_DIR/bin", "$this->FL_DIR/share/freeling");
		//Creating Client
		$this -> m = new MongoClient();
		//Currente database
		$this -> db = $this -> m -> test_database;
		$this -> tweets = $this -> db -> tw_data;
		$this -> entities = $this -> db -> entities;
		$this -> e_info = $this->db->entitie_info;
	}

	//Filtra y guarda las entidades obtenidas

	function save_entitie($str) {
		$explode = explode(' ', $str, 5);
		//echo 'explode: <br />';
		//echo print_r($explode) . '<br />';

		if ($explode[2][0] == 'N') {
			$entitie = array('entitie' => $explode[0], 'tagging' => $explode[2], 'per' => $explode[3]);
			$this -> entities -> insert($entitie);
			$this->consult($explode[0]);
		}
		if (isset($explode[4]) && $explode[4] != " ") {
			$this -> save_entitie($explode[4]);
		}

	}

	// Analiza el texto y regresa un arreglo con cada componente del analisis
	function analyze($str) {
		$output = str_replace("\n", " ", $this -> a -> analyze_text($str));
		$this -> save_entitie($output);
	}

	//Consulta la entidad en freeling
	function consult($entitie) {
		// Freebase
		$service_url = 'https://www.googleapis.com/freebase/v1/search';
		$params = array('query' => $entitie, 'key' => 'AIzaSyDd7UQL1RzURIZfVouNq5IFtI2BLr_nRJk');
		$url = $service_url . '?' . http_build_query($params);
		$ch = curl_init();
		curl_setopt($ch, CURLOPT_URL, $url);
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
		$response = json_decode(curl_exec($ch), true);
		curl_close($ch);
		echo "Consultando: $entitie <br />";
		foreach ($response['result'] as $result) {
			//echo $result['name'] . '<br/>';
			echo "Resultados <br />";
			$result['entitie'] = $entitie;
			echo print_r($result) . '<br/>';
			$this->e_info->insert($result);
		}
	}

	function test() {
		foreach ($this->tweets->find() as $tweet) {
			$this -> analyze($tweet['text']);
		}
	}

}

$f = new Freeling();
$f -> test();
?>
