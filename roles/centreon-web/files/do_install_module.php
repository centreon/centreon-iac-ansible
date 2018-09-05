<?php
require_once('/usr/share/centreon/config/centreon.config.php');
require_once("/usr/share/centreon/www/class/centreon.class.php");
require_once("/usr/share/centreon/www/class/centreonDB.class.php");

$oreon = True;
$pearDB = new CentreonDB();
$name = 'centreon-pp-manager';
$path = '/usr/share/centreon/www/include/options/oreon/modules/';

require_once("/usr/share/centreon/www/include/common/common-Func.php");
require_once($path ."DB-Func.php");

include_once("/usr/share/centreon/www/modules/".$name."/conf.php");

$upgrade_ok = false;
$insert_ok = insertModuleInDB($name, $module_conf[$name]);
if ($insert_ok) {
    echo "Module installed and registered\n";
    /*
    * SQL insert if need
    */
    $sql_file = "install.sql";
    $sql_file_path = "/usr/share/centreon/www/modules/".$name."/sql/";
    if (
      $module_conf[$name]["sql_files"] && file_exists($sql_file_path.$sql_file)
    ) {
        execute_sql_file($sql_file, $sql_file_path);
        echo "SQL file included\n";
    }
    /*
     * PHP execution if need
     */
    $php_file = "install.php";
    $php_file_path = "/usr/share/centreon/www/modules/".$name."/php/".$php_file;
    if ($module_conf[$name]["php_files"] && file_exists($php_file_path)) {
        echo "PHP file included\n";
        include_once($php_file_path);
    }
}

?>
