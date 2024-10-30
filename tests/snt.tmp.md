
---
title: snt
---


# snt

Version: 86
<br>Contact: Centre for Environmental Data Analysis; support@ceda.ac.uk


## Description:

This table is built by from snt.xml. This is not complete, but an excerpt!




## Modifications

Standard names can be modified by qualifications and transformations. Qualification do not change the unit of a standard name, where a transformation may change the unit.


### Qualification

[[surface]] [[component]] standard_name [at [surface]] [in [medium]] [due to [process]] [assuming [condition]]


#### Surface
Valid values: toa, tropopause, surface

A surface is defined as a function of horizontal position. Surfaces which are defined using a coordinate value (e.g. height of 1.5 m) are indicated by a single-valued coordinate variable, not by the standard name. In the standard name, some surfaces are named by single words which are placed at the start: toa (top of atmosphere), tropopause, surface. Other surfaces are named by multi-word phrases put after at: at_adiabatic_condensation_level, at_cloud_top, at_convective_cloud_top, at_cloud_base, at_convective_cloud_base, at_freezing_level, at_ground_level, at_maximum_wind_speed_level, at_sea_floor, at_sea_ice_base, at_sea_level, at_top_of_atmosphere_boundary_layer, at_top_of_atmosphere_model, at_top_of_dry_convection. The surface called "surface" means the lower boundary of the atmosphere. sea_level means mean sea level, which is close to the geoid in sea areas. ground_level means the land surface (beneath the snow and surface water, if any). cloud_base refers to the base of the lowest cloud. cloud_top refers to the top of the highest cloud. Fluxes at the top_of_atmosphere_model differ from TOA fluxes only if the model TOA fluxes make some allowance for the atmosphere above the top of the model; if not, it is usual to give standard names with toa to the fluxes at the top of the model atmosphere.


#### Component
Valid values: upward, downward, northward, southward, eastward, westward, x, y

The direction of the spatial component of a vector is indicated by one of the words upward, downward, northward, southward, eastward, westward, x, y. The last two indicate directions along the horizontal grid being used when they are not true longitude and latitude (if there is a rotated pole, for instance). If the standard name indicates a tensor quantity, two of these direction words may be included, applying to two of the spatial dimensions Z Y X, in that order. If only one component is indicated for a tensor, it means the flux in the indicated direction of the magnitude of the vector quantity in the plane of the other two spatial dimensions. The names of vertical components of radiative fluxes are prefixed with net_, thus: net_downward and net_upward. This treatment is not applied for any kinds of flux other than radiative. Radiative fluxes from above and below are often measured and calculated separately, the "net" being the difference. Within the atmosphere, radiation from below (not net) is indicated by a prefix of upwelling, and from above with downwelling. For the top of the atmosphere, the prefixes incoming and outgoing are used instead.,


#### Surface
Valid values: adiabatic_condensation_level, cloud_top, convective_cloud_top, cloud_base, convective_cloud_base, freezing_level, ground_level, maximum_wind_speed_level, sea_floor, sea_ice_base, sea_level, top_of_atmosphere_boundary_layer, top_of_atmosphere_model, top_of_dry_convection

A surface is defined as a function of horizontal position. Surfaces which are defined using a coordinate value (e.g. height of 1.5 m) are indicated by a single-valued coordinate variable, not by the standard name. In the standard name, some surfaces are named by single words which are placed at the start: toa (top of atmosphere), tropopause, surface. Other surfaces are named by multi-word phrases put after at: at_adiabatic_condensation_level, at_cloud_top, at_convective_cloud_top, at_cloud_base, at_convective_cloud_base, at_freezing_level, at_ground_level, at_maximum_wind_speed_level, at_sea_floor, at_sea_ice_base, at_sea_level, at_top_of_atmosphere_boundary_layer, at_top_of_atmosphere_model, at_top_of_dry_convection. The surface called "surface" means the lower boundary of the atmosphere. sea_level means mean sea level, which is close to the geoid in sea areas. ground_level means the land surface (beneath the snow and surface water, if any). cloud_base refers to the base of the lowest cloud. cloud_top refers to the top of the highest cloud. Fluxes at the top_of_atmosphere_model differ from TOA fluxes only if the model TOA fluxes make some allowance for the atmosphere above the top of the model; if not, it is usual to give standard names with toa to the fluxes at the top of the model atmosphere.


#### Medium
Valid values: air, atmosphere_boundary_layer, mesosphere, sea_ice, sea_water, soil, soil_water, stratosphere, thermosphere, troposphere

A medium indicates the local medium or layer within which an intensive quantity applies: in_air, in_atmosphere_boundary_layer, in_mesosphere, in_sea_ice, in_sea_water, in_soil, in_soil_water, in_stratosphere, in_thermosphere, in_troposphere.


#### Process
Valid values: advection, convection, deep_convection, diabatic_processes, diffusion, dry_convection, gravity_wave_drag, gyre, isostatic_adjustment, large_scale_precipitation, longwave_heating, moist_convection, overturning, shallow_convection, shortwave_heating, thermodynamics

The specification of a physical process by the phrase due_to_process means that the quantity named is a single term in a sum of terms which together compose the general quantity named by omitting the phrase. Possibilites are: due_to_advection, due_to_convection, due_to_deep_convection, due_to_diabatic_processes, due_to_diffusion, due_to_dry_convection, due_to_gravity_wave_drag, due_to_gyre, due_to_isostatic_adjustment, due_to_large_scale_precipitation, due_to_longwave_heating, due_to_moist_convection, due_to_overturning, due_to_shallow_convection, due_to_shortwave_heating, due_to_thermodynamics (referring to sea ice freezing and melting).


#### Condition
Valid values: clear_sky, deep_snow, no_snow

A phrase assuming_condition indicates that the named quantity is the value which would obtain if all aspects of the system were unaltered except for the assumption of the circumstances specified by the condition. Possibilities are assuming_clear_sky, assuming_deep_snow, assuming_no_snow.


### Transformations

| Rule | Units | Meaning |
|---------------|:-------------|:------------|
| change_over_time_in_X | [X] | change in a quantity X over a time-interval, which should be defined by the bounds of the time coordinate. |
| C_derivative_of_X | [X]/[C] | derivative of X with respect to distance in the component direction, which may be northward, southward, eastward, westward, x or y. The last two indicate derivatives along the axes of the grid, in the case where they are not true longitude and latitude. |



## Standard Names

| Standard Name | Vector/Scalar |     Units     | Description |
|---------------|:-------------:|:--------------|:------------|
| acoustic_area_backscattering_strength_in_sea_water | ? | 1 | Acoustic area backscattering strength is 10 times the log10 of the ratio of the area backscattering coefficient to the reference value, 1 (m2 m-2). Area backscattering coefficient is the integral of the volume backscattering coefficient over a defined distance. Volume backscattering coefficient is the linear form of acoustic_volume_backscattering_strength_in_sea_water. For further details see MacLennan et. al (2002) doi:10.1006/jmsc.2001.1158. |
| acoustic_centre_of_mass_in_sea_water | ? | m | Acoustic centre of mass is the average of all sampled depths weighted by their volume backscattering coefficient. Volume backscattering coefficient is the linear form of acoustic_volume_backscattering_strength_in_sea_water. For further details see Urmy et. al (2012) doi:10.1093/icesjms/fsr205. |
| acoustic_equivalent_area_in_sea_water | ? | m | Acoustic equivalent area is the squared area backscattering coefficient divided by the depth integral of squared volume backscattering coefficient. Area backscattering coefficient is the integral of the volume backscattering coefficient over a defined distance. Volume backscattering coefficient is the linear form of acoustic_volume_backscattering_strength_in_sea_water. The parameter is computed to provide a value that represents the area that would be occupied if all data cells contained the mean density and is the reciprocal of acoustic_index_of_aggregation_in_sea_water. For further details see Urmy et. al (2012) doi:10.1093/icesjms/fsr205 and Woillez et. al (2007) doi.org/10.1093/icesjms/fsm025. |
| acoustic_index_of_aggregation_in_sea_water | ? | 1/m | Acoustic index of aggregation is the depth integral of squared volume backscattering coefficient divided by the squared area backscattering coefficient. Volume backscattering coefficient is the linear form of acoustic_volume_backscattering_strength_in_sea_water. Area backscattering coefficient is the integral of the volume backscattering coefficient over a defined distance. The parameter is computed to provide a value that represents the patchiness of biomass in the water column in the field of fisheries acoustics - the value is high when small areas are much denser than the rest of the distribution. The parameter is also the reciprocal of acoustic_equivalent_area_in_sea_water. For further details see Urmy et. al (2012) doi:10.1093/icesjms/fsr205 and Woillez et. al (2007) doi.org/10.1093/icesjms/fsm025. |
| acoustic_inertia_in_sea_water | ? | 1/m^2 | Acoustic inertia is the sum of squared distances from the acoustic_centre_of_mass weighted by the volume backscattering coefficient at each distance and normalized by the total area backscattering coefficient. Volume backscattering coefficient is the linear form of acoustic_volume_backscattering_strength_in_sea_water. Area backscattering coefficient is the integral of the volume backscattering coefficient over a defined distance. For further details see Urmy et. al (2012) doi:10.1093/icesjms/fsr205 and Bez and Rivoirard (2001) doi:10.1016/S0165-7836(00)00241-1. |
| acoustic_proportion_occupied_in_sea_water | ? | 1 | Acoustic proportion occupied is occupied volume divided by the volume sampled. Occupied volume is the integral of the ratio of acoustic_volume_backscattering_strength_in_sea_water above -90 dB to the reference value, 1 m2 m-2. For further details see Urmy et. al (2012) doi:10.1093/icesjms/fsr205. |
| acoustic_signal_roundtrip_travel_time_in_sea_water | ? | s | The quantity with standard name acoustic_signal_roundtrip_travel_time_in_sea_water is the time taken for an acoustic signal to propagate from the emitting instrument to a reflecting surface and back again to the instrument. In the case of an instrument based on the sea floor and measuring the roundtrip time to the sea surface, the data are commonly used as a measure of ocean heat content. |
| acoustic_target_strength_in_sea_water | ? | 1 | Target strength is 10 times the log10 of the ratio of backscattering cross-section to the reference value, 1 m2. Backscattering cross-section is a parameter computed from the intensity of the backscattered sound wave relative to the intensity of the incident sound wave. For further details see MacLennan et. al (2002) doi:10.1006/jmsc.2001.1158. |
| acoustic_volume_backscattering_strength_in_sea_water | ? | 1 | Acoustic volume backscattering strength is 10 times the log10 of the ratio of the volume backscattering coefficient to the reference value, 1 m-1. Volume backscattering coefficient is the integral of the backscattering cross-section divided by the volume sampled. Backscattering cross-section is a parameter computed from the intensity of the backscattered sound wave relative to the intensity of the incident sound wave. The parameter is computed to provide a measurement that is proportional to biomass density per unit volume in the field of fisheries acoustics. For further details see MacLennan et. al (2002) doi:10.1006/jmsc.2001.1158. |
| aerodynamic_particle_diameter | ? | m | The diameter of a spherical particle with density 1000 kg m-3 having the same aerodynamic properties as the particles in question. |
