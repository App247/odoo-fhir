# -*- coding: utf-8 -*-

from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class CountryRegionType(models.Model):
    _name = "hc.vs.country.region.type"
    _description = "Region Type"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Region Type",
        help="Type of grouping of divisions (e.g. Region in the US).")
    country_id = fields.Many2one(
        comodel_name="res.country",
        string="Country",
        help="Country that maintains the region type.")

class CountryRegion(models.Model):
    _name = "hc.vs.country.region"
    _description = "Region"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Region",
        help="A grouping of divisions (e.g. West and Midwest in the US).")
    type_id = fields.Many2one(
        comodel_name="hc.vs.country.region.type",
        string="Region Type",
        help="Type of grouping of regions (e.g. Region in the US).")
    country_id = fields.Many2one(
        comodel_name="res.country",
        string="Country",
        help="Country (can be ISO-3166 3-letter code).")

class CountryDivisionType(models.Model):
    _name = "hc.vs.country.division.type"
    _description = "Division Type"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="Division Type",
        help="Type of grouping of principal subdivisions (e.g., Division in the US).")
    country_id = fields.Many2one(
        comodel_name="res.country",
        string="Country",
        help="Country that maintains the division type.")

class CountryDivision(models.Model):
    _name = "hc.vs.country.division"
    _description = "Division"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
       string="Division",
       help="A grouping of principal subdivisions (e.g., England in the UK, West in the US).")
    type_id = fields.Many2one(
        comodel_name="hc.vs.country.division.type",
        string="Division Type",
        help="Type of grouping of principal subdivisions (e.g., Division in the US).")
    region_id = fields.Many2one(
        comodel_name="hc.vs.country.region",
        string="Region",
        help="A grouping of divisions or states (e.g. West, Midwest).")
    country_id = fields.Many2one(
        comodel_name="res.country",
        string="Country",
        help="Country (can be ISO-3166 3-letter code).")

class CountryStateType(models.Model):
    _name = "hc.vs.country.state.type"
    _description = "State/Province Type"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
		string="State/Province Type",
        help="Type of principal subdivision of a country (e.g., state, province, two-tier county).")
    country_id = fields.Many2one(
    	comodel_name="res.country",
    	string="Country",
    	help="Country that maintains the state/province type.")

class CountryState(models.Model):
    _name = "res.country.state"
    _description = "Country State"
    _inherit = ["res.country.state"]

    name = fields.Char(
        string="Name",
        help="Sub-unit (i.e., primary subdivision) of a country (abreviations ok).")
    code = fields.Char(
        string="Code",
        help="The suffix of the ISO 3166-2 code that uniquely identifies a principal subdivision (e.g., states or provinces) within a country.")
    numeric_code = fields.Char(
        string="Numeric Code",
        help="Numeric code that uniquely identifies a principal subdivision (e.g., state or province) within a country.")
    type_id = fields.Many2one(
        comodel_name="hc.vs.country.state.type",
        string="State Type",
        help="Type of principal subdivision of a country (e.g., state, province).")
    division_id = fields.Many2one(
        comodel_name="hc.vs.country.division",
        string="Division",
        help="Group of primary subdivisions (e.g., Pacific and Mountain in the US).")
    region_id = fields.Many2one(
       related="division_id.region_id",
       string="Region",
       help="A grouping of divisions or states (e.g. West, Midwest).")
    country_id = fields.Many2one(
       related="division_id.country_id",
       string="Country",
       help="Country (can be ISO-3166 3-letter code).")
    source_id = fields.Many2one(
        comodel_name="res.partner",
        string="Source",
        help="The source of the definition of the code.")
    system = fields.Char(
        string="Source URL",
        help="Web address of the source of the code.")

class CountryDistrictType(models.Model):
    _name = "hc.vs.country.district.type"
    _description = "District Type"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
       string="District/County Type",
       help="Type of administrative area (e.g., In US, county).")
    country_id = fields.Many2one(
        comodel_name="res.country",
        string="Country",
        help="Country that maintains the district type.")

class CountryDistrict(models.Model):
    _name = "hc.vs.country.district"
    _description = "District"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="District/County",
        help="Top-level administrative area of a principal subdivision (e.g., County in US State).")
    type_id = fields.Many2one(
        comodel_name="hc.vs.country.district.type",
        string="District Type",
        help="Type of administrative area (e.g., In US, county or parish).")
    city_ids = fields.Many2many(
        comodel_name="hc.vs.country.city",
        string="Cities/Places",
        help="The name of the city, town, village or other community or delivery center.")
    state_id = fields.Many2one(
        comodel_name="res.country.state",
        string="State",
        help="Sub-unit of country (abbreviations ok).")
    division_id = fields.Many2one(
        related="state_id.division_id",
        string="Division",
        help="Group of primary subdivisions (e.g., Pacific and Mountain in the US).")
    region_id = fields.Many2one(
        related="state_id.region_id",
        string="Region",
        help="A grouping of divisions or states (e.g. West, Midwest).")
    country_id = fields.Many2one(
        related="state_id.country_id",
        string="Country",
        help="Country (can be ISO-3166 3-letter code).")

class CountryCityType(models.Model):
    _name = "hc.vs.country.city.type"
    _description = "City/Place Type"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
       string="City/Place Type",
       help="Type of place or district/county subdivision (e.g., city, town).")
    country_id = fields.Many2one(
        comodel_name="res.country",
        string="Country",
        help="Country that maintains the city/place type.")

class CountryCityCategory(models.Model):
    _name = "hc.vs.country.city.category"
    _description = "City/Place Category"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
       string="City/Place Category",
       help="Category of place or district/county subdivision (e.g., census designated place, incorporated place).")
    country_id = fields.Many2one(
        comodel_name="res.country",
        string="Country",
        help="Country that maintains the city/place category.")

class CountryCityStatus(models.Model):
    _name = "hc.vs.country.city.status"
    _description = "City/Place Functional Status"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
       string="City/Place Functional Status",
       help="Status of a place from a legal and/or statistical perspective.")
    country_id = fields.Many2one(
        comodel_name="res.country",
        string="Country",
        help="Country that maintains the city/place functional status.")

class CountryCity(models.Model):
    _name = "hc.vs.country.city"
    _description = "City/Place"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
        string="City/Place",
        help="The name of the city, town, village or other community or delivery center.")
    numeric_code = fields.Char(
        string="Numeric Code",
        help="Code that uniquely identifies a place within a primary subdivision (e.g. In US, 5-digit FIPS Place Code).")
    type_id = fields.Many2one(
        comodel_name="hc.vs.country.city.type",
        string="Place Type",
        help="Type of place or county subdivision (e.g., city, town).")
    category_id = fields.Many2one(
        comodel_name="hc.vs.country.city.category",
        string="Place Category",
        help="Category of place or district/county subdivision (e.g., census designated place, incorporated place).")
    status_id = fields.Many2one(
        comodel_name="hc.vs.country.city.status",
        string="Functional Status",
        help="Status of a place from a legal and/or statistical perspective.")
    postal_code_ids = fields.Many2many(
        comodel_name="hc.vs.country.postal.code",
        string="Postal Codes",
        help="A string of numbers or letters and numbers that are added to a postal address to assist the sorting of mail.")
    is_primary_postal_code_city = fields.Boolean(
        string="Primary City",
        help="Indicates if this city is the primary city for a postal code.")
    district_ids = fields.Many2many(
        comodel_name="hc.vs.country.district",
        string="Districts/Counties",
        help="The name of the administrative area (e.g., county).")
    state_id = fields.Many2one(
        comodel_name="res.country.state",
        string="State",
        help="Sub-unit of country (abbreviations ok).")
    division_id = fields.Many2one(
        related="state_id.division_id",
        string="Division",
        help="Group of primary subdivisions (e.g., Pacific and Mountain in the US).")
    region_id = fields.Many2one(
        related="state_id.region_id",
        string="Region",
        help="A grouping of divisions or states (e.g. West, Midwest).")
    country_id = fields.Many2one(
        related="state_id.country_id",
        string="Country",
        help="Country (can be ISO-3166 3-letter code).")

class CountryPostalCodeType(models.Model):
    _name = "hc.vs.country.postal.code.type"
    _description = "Postal/ZIP Code Type"
    _inherit = ["hc.value.set.contains"]

    name = fields.Char(
       string="Postal/ZIP Code Type",
       help="Type of postal code (e.g., standard, PO Box).")
    country_id = fields.Many2one(
       comodel_name="res.country",
       string="Postal Code Country Owner",
       help="Country that maintains the postal code type.")

class CountryPostalCode(models.Model):
    _name = "hc.vs.country.postal.code"
    _description = "Postal Code"
    _inherit = ["hc.value.set.contains"]
    _rec_name = "postal_code"

    postal_code = fields.Char(
        string="Postal/ZIP Code",
        help="A group of numbers or letters and numbers that are added to a postal address to assist the sorting of mail.")
    # name = fields.Char(
    #     string="Postal/ZIP Code",
    #     help="A group of numbers or letters and numbers that are added to a postal address to assist the sorting of mail.")
    name = fields.Char(
        compute="_compute_code",
        store="True")
    code = fields.Char(
        compute="_compute_code",
        store="True")
    postal_place = fields.Char(
        string="Place",
        help="A geographic point of interest associated with a postal code.")
    type_id = fields.Many2one(
        comodel_name="hc.vs.country.postal.code.type",
        string="Postal Code Type",
        help="Type of postal code (e.g., standard, PO Box).")
    is_decommissioned = fields.Boolean(
        string="Decommission",
        help="Indicates if the postal code is not in active use.")
    latitude = fields.Float(
        string="Latitude",
        help="Average geographic latitude of the postal code.")
    longitude = fields.Float(
        string="Longitude",
        help="Average geographic longitude of the postal code.")
    postal_code_owner_country_id = fields.Many2one(
        comodel_name="res.country",
        string="Postal Code Country Owner",
        help="Country that maintains the postal code.")
    city_ids = fields.Many2many(
        comodel_name="hc.vs.country.city",
        string="Cities/Places",
        help="The name of the city, town, village or other community or delivery center.")
    district_ids = fields.Many2many(
        comodel_name="hc.vs.country.district",
        string="Districts/Counties",
        help="The name of the administrative area (e.g., county).")
    state_ids = fields.Many2many(
        comodel_name="res.country.state",
        string="State",
        help="Sub-unit (i.e., primary subdivision) of a country (abreviations ok).")
    division_id = fields.Many2one(
        comodel_name="hc.vs.country.division",
        string="Division",
        help="Group of primary subdivisions (e.g., Pacific and Mountain in the US).")
    region_id = fields.Many2one(
        related="division_id.region_id",
        string="Region",
        help="A grouping of divisions or states (e.g. West, Midwest).")
    country_id = fields.Many2one(
        related="division_id.country_id",
        string="Country",
        help="Country (can be ISO-3166 3-letter code).")

    @api.depends('postal_code')
    def _compute_code(self):
        comp_code = '/code'
        comp_name = '/name'
        for hc_vs_country_postal_code in self:
            if hc_vs_country_postal_code.postal_code:
                comp_code = hc_vs_country_postal_code.postal_code or ''
                comp_name = hc_vs_country_postal_code.postal_code or ''
            hc_vs_country_postal_code.code = comp_code
            hc_vs_country_postal_code.name = comp_name

class AddressUse(models.Model):
    _name = "hc.address.use"
    _description = "Address Use"
    _inherit = ["hc.basic.association"]

    use = fields.Selection(
        string="Use",
        selection=[
            ("home", "Home"),
            ("work", "Work"),
            ("temp", "Temp"),
            ("old", "Old")],
        help="The purpose of this address.")
    type = fields.Selection(
        string="Type",
        selection=[
            ("postal", "Postal"),
            ("physical", "Physical"),
            ("both", "Both")],
        default="both",
        help="Distinguishes between physical addresses (those you can visit) and mailing addresses (e.g. PO Boxes and care-of addresses). Most addresses are both.")

class Address(models.Model):
    _name = "hc.address"
    _description = "Address"
    _inherit = ["hc.element"]
    _rec_name = "text"

    text = fields.Char(
        string="Full Address",
        compute="_compute_full_address",
        store="True",
        help="A full text representation of the address.")
    line1 = fields.Char(
        string="Address Line 1",
        help="Street name, number, direction & P.O. Box etc.")
    line2 = fields.Char(
        string="Address Line 2",
        help="Street name, number, direction & P.O. Box etc.")
    line3 = fields.Char(
        string="Address Line 3",
        help="Street name, number, direction & P.O. Box etc.")
    city_id = fields.Many2one(
        comodel_name="hc.vs.country.city",
        string="City/Place",
        help="The name of the city, town, village or other community or delivery center.")
    district_id = fields.Many2one(
        comodel_name="hc.vs.country.district",
        string="District/County",
        help="The name of the administrative area (e.g., county).")
    state_id = fields.Many2one(
        comodel_name="res.country.state",
        string="State/Province",
        help="Sub-unit (i.e., primary subdivision) of a country (abreviations ok).")
    postal_code_id = fields.Many2one(
        comodel_name="hc.vs.country.postal.code",
        string="Postal/ZIP Code",
        help="Postal code for area.")
    division_id = fields.Many2one(
        related="postal_code_id.division_id",
        string="Division",
        help="Group of states (e.g., Pacific, Mountain).")
    region_id = fields.Many2one(
        related="postal_code_id.region_id",
        string="Region",
        help="First level subdivision of a country (e.g. West, Midwest).")
    country_id = fields.Many2one(
        related="postal_code_id.country_id",
        string="Country",
        help="Country (can be ISO 3166 3 letter code).")

    # Extension attribute
    geolocation_id = fields.Many2one(
        comodel_name="hc.address.geolocation",
        string="Geolocation",
        help="Geolocation associated with this Address.")

    @api.depends('line1', 'line2', 'line3', 'city_id', 'postal_code_id', 'district_id', 'state_id', 'division_id', 'region_id', 'country_id')
    def _compute_full_address(self):
        comp_full_address = '/'
        for hc_address in self:
            if hc_address.line1:
                comp_full_address = hc_address.line1 or ''
            if hc_address.line2:
                comp_full_address = comp_full_address + ", " + hc_address.line2 or ''
            if hc_address.line3:
                comp_full_address = comp_full_address + ", " + hc_address.line3 or ''
            if hc_address.city_id:
                comp_full_address = comp_full_address + ", " + hc_address.city_id.name or ''
            if hc_address.postal_code_id:
                comp_full_address = comp_full_address + ", " + hc_address.postal_code_id.postal_code or ''
            if hc_address.district_id:
                comp_full_address = comp_full_address + ", " + hc_address.district_id.name or ''
            if hc_address.state_id:
                comp_full_address = comp_full_address + ", " + hc_address.state_id.code or ''
            if hc_address.division_id:
                comp_full_address = comp_full_address + ", " + hc_address.division_id.name or ''
            if hc_address.region_id:
                comp_full_address = comp_full_address + ", " + hc_address.region_id.name or ''
            if hc_address.country_id:
                comp_full_address = comp_full_address + ", " + hc_address.country_id.name or ''
            hc_address.text = comp_full_address

    # @api.depends('line1','line2','line3','city_id','postal_code_id', 'district_id', 'state_id', 'division_id', 'region_id', 'country_id')
    # def _compute_full_address(self):
    #     address = ''
    #     lines = ''
    #     line1 = self.line1 and self.line1 or ''
    #     line2 = self.line2 and ', '+self.line2 or ''
    #     line3 = self.line3 and ', '+self.line3 or ''
    #     city = self.city_id and ', '+self.city_id.name or ''
    #     postal = self.postal_code_id and ', '+self.postal_code_id.name or ''
    #     district = self.district_id and ', '+self.district_id.name or ''
    #     state = self.state_id and ', '+self.state_id.code or ''
    #     division = self.division_id and ', '+self.division_id.name or ''
    #     region = self.region_id and ', '+self.region_id.name or ''
    #     country = self.country_id and ', '+self.country_id.name or ''
    #     lines = line1+line2+line3+city+postal+district+state+division+region+country+lines
    #     self.text = lines


class AddressGeolocation(models.Model):
    _name = "hc.address.geolocation"
    _description = "Address Geolocation"

    name = fields.Char(
        string="Name",
        compute="_compute_name",
        store="True",
        help="Text representation of the geolocation. Latitude + Longitude.")
    latitude = fields.Float(
        string="Latitude",
        digits_compute=dp.get_precision('Geolocation'),
        required="True",
        help="Latitude with WGS84 datum, aka north-south position. North latitude is positive. Format: Decimal. Example: +55.6124")
    latitude_direction = fields.Selection(
        string="Latitude Direction",
        required="True",
        selection=[
            ("+", "North"),
            ("-", "South")],
        default="+",
        help="The latitude direction.")
    longitude = fields.Float(
        string="Longitude",
        digits_compute=dp.get_precision('Geolocation'),
        required="True",
        help="Longitude with WGS84 datum, aka east-west position. East longitude is positive. Format: Decimal. Example: -100.2345")
    longitude_direction = fields.Selection(
        string="Longitude Direction",
        required="True",
        selection=[
            ("+", "East"),
            ("-", "West")],
        default="+",
        help="Direction relative to the prime meridian.")

    _sql_constraints = [
        ('latitude_range',
        'CHECK(latitude >= 0 and latitude <= 90)',
        'Latitude should be 0 to 90.'),

        ('longitude_range',
        'CHECK(longitude >= 0 and longitude <= 180)',
        'Longitude should be 0 to 180.')]

    @api.depends('latitude', 'longitude')
    def _compute_name(self):
        comp_name = '/'
        for hc_address_geolocation in self:
            if hc_address_geolocation.latitude:
                comp_name = str(hc_address_geolocation.latitude_direction) + str(hc_address_geolocation.latitude)
                # comp_name = str(hc_address_geolocation.latitude) + "°" or ''
            if hc_address_geolocation.longitude:
                comp_name = comp_name + " " + str(hc_address_geolocation.longitude_direction) + str(hc_address_geolocation.longitude)
                # comp_name = comp_name + ", " + str(hc_address_geolocation.longitude) + "°" or ''
            hc_address_geolocation.name = comp_name
