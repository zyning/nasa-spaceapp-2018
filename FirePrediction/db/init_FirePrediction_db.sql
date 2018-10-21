DROP DATABASE firecaster_db;
set datestyle to SQL,DMY;

CREATE DATABASE firecaster_db;
\connect firecaster_db;
CREATE EXTENSION postgis;
CREATE EXTENSION fuzzystrmatch;
CREATE EXTENSION postgis_tiger_geocoder CASCADE;

-- nyc_fire_predictions
CREATE TABLE fire_predictions (
  id serial primary key,
  nyc_tracts jsonb
);

-- nyc_weather
CREATE TABLE nyc_weather( 
	observation_date_time character varying(12),
	mintempm numeric,
	maxtempm numeric,
	humidity numeric,
	snow numeric,
	snowdepthm numeric,
	meanpressurem numeric,
	meanwindspdm numeric,
	precipm numeric,
	rain numeric
);

-- nyc_census
CREATE TABLE nyc_census( 
	NAME character varying(100),
	B16001_001E numeric,
	B01001_027E numeric,
	B02001_007E numeric,
	B25034_001E numeric,
	B01001H_027E numeric,
	B02001_003E numeric,
	B11011_001E numeric,
	B25034_009E numeric,
	B23003_001E numeric,
	B23006_001E numeric,
	B02001_002E numeric,
	B25010_001E numeric,
	B01001H_003E numeric,
	B25064_001M numeric,
	B01001C_003E numeric,
	B25077_001E numeric,
	B11001_002E numeric,
	B02001_006E numeric,
	B19025_001E numeric,
	B19001_001E numeric,
	B25034_006E numeric,
	B25001_001E numeric,
	B25004_002E numeric,
	B01001_003E numeric,
	B05009_012E numeric,
	B25034_010E numeric,
	B25075_025E numeric,
	B05009_019E numeric,
	B19013_001E numeric,
	B01001C_027E numeric,
	B25021_001E numeric,
	B02001_005E numeric,
	B25034_007E numeric,
	B25004_001E numeric,
	B01002_001E numeric,
	B25004_005E numeric,
	B05009_005E numeric,
	B06001_049E numeric,
	B01001I_001E numeric,
	B05009_009E numeric,
	B06012_003E numeric,
	B06012_002E numeric,
	B01001_001E numeric,
	B01001B_003E numeric,
	B02001_004E numeric,
	B25058_001E numeric,
	B01001B_027E numeric,
	B25034_008E numeric,
	state character varying(40),	
	county character varying(40),
	tract character varying(40)
);

-- NYC Fire Incidents 
CREATE TABLE nyc_streets_segments( 
	street character varying(100),
	right_bloc character varying(40),
	left_block character varying(40),
	geom public.geometry(MultiLineString,2263)
);

-- NYC Fire Incidents 
CREATE TABLE nyc_fire_incident( 
	im_incident_key character varying(30),
	incident_date_time date,
	street_highway character varying(100),
	address character varying(100)
);

-- NYC Tract
CREATE TABLE nyc_tract( 
	geoid character varying(30),
	name character varying(30),
	countyfp character varying(20),
	tractce character varying(20),
	statefp character varying(20),
	namelsad character varying(41),
	lsad character varying(2),
	cdsessn character varying(3),
	mtfcc character varying(5),
	funcstat character varying(1),
	aland double precision,
	awater double precision, 
	intptlat character varying(11),
	intptlon character varying(12),
	geom public.geometry(MultiPolygon,2263)

);

-- NYC Mappluto
CREATE TABLE nyc_map_pluto_16v1( 
	gid BIGINT, 
	borough character varying(2), 
	block integer, 
	lot smallint, 
	cd smallint, 
	ct2010 character varying(7), 
	cb2010 character varying(5), 
	schooldist character varying(2), 
	council smallint, 
	zipcode integer, 
	firecomp character varying(4), 
	policeprct smallint, 
	healtharea smallint, 
	sanitboro character varying(1), 
	sanitdist character varying(2), 
	sanitsub character varying(2), 
	address character varying(28), 
	zonedist1 character varying(9), 
	zonedist2 character varying(9), 
	zonedist3 character varying(9), 
	zonedist4 character varying(9), 
	overlay1 character varying(4), 
	overlay2 character varying(4), 
	spdist1 character varying(6), 
	spdist2 character varying(6), 
	ltdheight character varying(5), 
	allzoning1 character varying(27), 
	allzoning2 character varying(21), 
	splitzone character varying(1), 
	bldgclass character varying(2), 
	landuse character varying(2), 
	easements smallint, 
	ownertype character varying(1), 
	ownername character varying(21), 
	lotarea integer, 
	bldgarea integer, 
	comarea integer, 
	resarea integer, 
	officearea integer, 
	retailarea integer, 
	garagearea integer, 
	strgearea integer, 
	factryarea integer, 
	otherarea integer, 
	areasource character varying(1), 
	numbldgs integer, 
	numfloors numeric, 
	unitsres integer, 
	unitstotal integer, 
	lotfront numeric, 
	lotdepth numeric, 
	bldgfront numeric, 
	bldgdepth numeric, 
	ext character varying(2), 
	proxcode character varying(1), 
	irrlotcode character varying(1), 
	lottype character varying(1), 
	bsmtcode character varying(1), 
	assessland numeric, 
	assesstot numeric, 
	exemptland numeric, 
	exempttot numeric, 
	yearbuilt smallint, 
	builtcode character varying(1), 
	yearalter1 smallint, 
	yearalter2 smallint, 
	histdist character varying(40), 
	landmark character varying(35), 
	builtfar numeric, 
	residfar numeric, 
	commfar numeric, 
	facilfar numeric, 
	borocode integer, 
	bbl numeric, 
	condono integer, 
	tract2010 character varying(6), 
	xcoord integer, 
	ycoord integer, 
	zonemap character varying(3), 
	zmcode character varying(1), 
	sanborn character varying(8), 
	taxmap character varying(5), 
	edesignum character varying(5), 
	appbbl numeric, 
	appdate character varying(10), 
	plutomapid character varying(1), 
	version character varying(4), 
	mappluto_f smallint, 
	shape_leng numeric, 
	shape_area numeric, 
	geom public.geometry(MultiPolygon,2263) 
);
