<?php

function glint($file){
  global $SYS_CONF;
  system('python ' . $SYS_CONF['glint'] . ' --nojsdoc '  . $file);
};


function jsdoc($file){
  global $SYS_CONF;
  $base = dirname(__FILE__);

  $command =  'java -jar ' . $SYS_CONF['jsdoc'] . ' ' . $base . '/../tools/jsdoc-toolkit/app/run.js -a -t=' . $base . '/../tools/jsdoc-toolkit/templates/jsdoc -d=' . $base . '/../doc ' . $file;

  system($command);
}

?>