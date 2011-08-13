module('pyjs');


test('get dependency' , function(){
    addDependence('main' , '');
    addDependence('core' , '');
    addDependence('string' , 'main,core');
    addDependence('do' , 'main');
    addDependence('final' , 'do,string');
    var rs = ['core' , 'main' , 'do',  'string' , 'final'];

    deepEqual( getDependence('final') , rs , 'getDependence works right.');
});

