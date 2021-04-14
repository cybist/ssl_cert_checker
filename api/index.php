<?php
// composer require yosymfony/toml
require_once 'vendor/autoload.php';
use Yosymfony\Toml\Toml;

$configs = Toml::ParseFile(dirname(__FILE__) . '/../configs/common.toml');

$options = array(
    'create_if_missing' => true,
    'error_if_exists'    => false,
    'paranoid_checks'    => false,
    'block_cache_size'    => 8 * (2 << 20),
    'write_buffer_size' => 4<<20,
    'block_size'        => 4096,
    'max_open_files'    => 1000,
    'block_restart_interval' => 16,
    'compression'        => LEVELDB_SNAPPY_COMPRESSION,
    'comparator'        => NULL,
);

$readoptions = array(
    'verify_check_sum'    => false,
    'fill_cache'        => true,
    'snapshot'            => null
);

$writeoptions = array(
    'sync' => false
);

$db = new LevelDB($configs['APP_DIR'] . $configs['RESULT_DB'], $options, $readoptions, $writeoptions);
$results = [];
foreach ($configs['DOMAIN_LIST'] as $brand => $list) {
    isset($results[$brand]) or $results[$brand] = [];
    foreach ($list as $fqdn) {
        $result = $db->get($fqdn);
        $results[$brand][$fqdn] = $result;
    }
}
$checked_at = date('Y/m/d H:i:s', filemtime($configs['APP_DIR'] . $configs['RESULT_DB'] . '/LOCK'));
echo json_encode(['list' => $results, 'checked_at' => $checked_at], JSON_UNESCAPED_UNICODE);