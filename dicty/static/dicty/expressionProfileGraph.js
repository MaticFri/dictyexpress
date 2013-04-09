$(function () {

currentExperiment = {
	"species": "D. discoideum",
	"strain": "AX4",
	"growth": "KA"
};
profile = {
	// displayed genes
	"DDB_G0273069": [ 38517.390436, 10468.991257, 5120.999755, 4599.216053, 6008.108929, 9891.453052, 7006.916784 ],
	"DDB_G0279387": [ 55552.413897, 14083.098324, 3052.53189, 2937.61897, 1731.729698, 1948.400179, 1931.351379 ],
	"DDB_G0284861": [ 32727.034273, 19346.784749, 6438.15899, 9452.846883, 8899.117963, 8974.251067, 7498.366213 ],
	"DDB_G0285597": [ 43103.74384, 16338.426274, 3365.145447, 3168.372899, 1702.320396, 2161.586845, 2028.246308 ],
	"DDB_G0289025": [ 21680.492921, 7436.382207, 1663.542156, 1859.91882, 1147.012705, 1176.374009, 1183.427 ]
};

allGenes = {
	"... kind of comment": "this is just some genes, not all",
	"rab32C": {
		"name": "rab32C",
		"id": "DDB_G0275675",
		"jgi_id": 91127
	},
	"DDB_G0275849": {
		"name": "DDB_G0275849",
		"id": "DDB_G0275849",
		"jgi_id": 91130
	},
	"mobA": {
		"name": "mobA",
		"id": "DDB_G0278907",
		"jgi_id": 91135
	},
	"fray1": {
		"name": "fray1",
		"id": "DDB_G0278863",
		"jgi_id": 91138
	},
	"DDB_G0279247": {
		"name": "DDB_G0279247",
		"id": "DDB_G0279247",
		"jgi_id": 91142
	},
	"mrrA": {
		"name": "mrrA",
		"id": "DDB_G0271908",
		"jgi_id": 91918
	},
	"padA": {
		"name": "padA",
		"id": "DDB_G0286385",
		"jgi_id": 91927
	},
	"DDB_G0287001": {
		"name": "DDB_G0287001",
		"id": "DDB_G0287001",
		"jgi_id": 91930
	},
	"DDB_G0287073": {
		"name": "DDB_G0287073",
		"id": "DDB_G0287073",
		"jgi_id": 91932
	},
	"DDB_G0276545": {
		"name": "DDB_G0276545",
		"id": "DDB_G0276545",
		"jgi_id": 91936
	},
	"rab8A": {
		"name": "rab8A",
		"id": "DDB_G0280043",
		"jgi_id": 91938
	},
	"osbH": {
		"name": "osbH",
		"id": "DDB_G0283709",
		"jgi_id": 91950
	},
	"ndkC-1": {
		"name": "ndkC-1",
		"id": "DDB_G0273069",
		"jgi_id": 97095
	},
	"rpl21": {
		"name": "rpl21",
		"id": "DDB_G0279387",
		"jgi_id": 93065
	},
	"eif5a": {
		"name": "eif5a",
		"id": "DDB_G0284861",
		"jgi_id": 91781
	},
	"rps28": {
		"name": "rps28",
		"id": "DDB_G0285597",
		"jgi_id": 47614
	},
	"rps7": {
		"name": "rps7",
		"id": "DDB_G0289025",
		"jgi_id": 92493
	}
};
		var dataForSeries=[];
		for(ee in profile){
			dataForSeries.push(
			{
				name: ee,
				data: profile[ee]
			}
			);
		}
		
		
		
        $('#container').highcharts({
			credits: {enabled:false},			
            chart: {type: 'line'},
            title: {
                text: 'Expression Profile:',
                x: -20 //center
            },
            subtitle: {
                text: currentExperiment.species+' / '+currentExperiment.strain+' / '+currentExperiment.growth,
                x: -20
            },
            xAxis: {
			    title: {text: 'time [hrs]'},
				min: 0,
				max: 24,
				tickInterval: 2
            },
            yAxis: {
                title: {
                    text: 'Scaled Read Counts'
                },
				min:0,
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#808080'
                }],
				labels: {format: '{value}'}
            },
			tooltip: {
				shared: true,
                crosshairs: true,
                formatter: function() {
					var str = 'Time: <b>'+ this.x +'h';
					$.each(this.points, function(i, point) {
						str += '<br><span style="color:'+point.series.color+'; font-size:80%;">'+ point.series.name +': '+ point.y +'</span>';
					});
					return str;
				}
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'top',
                x: -10,
                y: 100,
                borderWidth: 0
            },
			plotOptions: {
				series: {
					pointStart: 0,
					pointInterval: 4 
				}
			},
			// get data
            series: dataForSeries
        });
    });