class CRS610AddTransformer:
    """
    Transformer for adding a new item to the CRS610 table.
    """
    def __init__(self):
        self._item = None

    def transform(self, row):
        if not row:
            return None

        self._item = row

        data = {
            "CUTM": self.get_customer_template(),
            "LNCD": self.get_language_code(),
            "CUNO": self.get_customer_number(),
            "CUNM": self.get_customer_name(),
            "CUA1": self.get_customer_address_1(),
            "CUA2": self.get_customer_address_2(),
            "CUA3": self.get_customer_address_3(),
            "CUA4": self.get_customer_address_4(),
            "PONO": self.get_postal_code(),
            "PHNO": self.get_phone_number(),
            "PHN2": self.get_phone_number_2(),
            "TFNO": self.get_fax_number(),
            "CUTP": self.get_customer_type(),
            "ALCU": self.get_search_key(),
            "YREF": self.get_reference(),
            "YRE2": self.get_reference_2(),
            "MAIL": self.get_email(),
            "CSCD": self.get_country_code(),
            "ECAR": self.get_state(),
            "CFC1": self.get_free_field_1(),
            "CFC2": self.get_free_field_2(),
            "CFC3": self.get_free_field_3(),
            "CFC4": self.get_free_field_4(),
            "CFC5": self.get_free_field_5(),
            "CFC6": self.get_free_field_6(),
            "CFC7": self.get_free_field_7(),
            "CFC8": self.get_free_field_8(),
            "CFC9": self.get_free_field_9(),
            "CFC0": self.get_free_field_10(),
            "CESA": self.get_sms_id(),
            "STAT": self.get_status(),
            "PWMT": self.get_password(),
            "IVGP": self.get_invoice_group(),
            "TOWN": self.get_city(),
            "CUSU": self.get_our_supplier_number_at_customer(),
            "FRCO": self.get_county_id(),
            "EDES": self.get_place(),
            "EALO": self.get_ean_location(),
            "RASN": self.get_rail_station(),
            "SPLE": self.get_standard_point_location_code(),
            "ERRM": self.get_error_message_if_status_12()
        }
        
        return data

    def get_customer_template(self):
        pass

    def get_language_code(self):
        pass

    def get_customer_number(self):
        pass

    def get_customer_name(self):
        pass

    def get_customer_address_1(self):
        pass

    def get_customer_address_2(self):
        pass

    def get_customer_address_3(self):
        pass

    def get_customer_address_4(self):
        pass

    def get_postal_code(self):
        pass

    def get_phone_number(self):
        pass

    def get_phone_number_2(self):
        pass

    def get_fax_number(self):
        pass

    def get_customer_type(self):
        pass

    def get_search_key(self):
        pass

    def get_reference(self):
        pass

    def get_reference_2(self):
        pass

    def get_email(self):
        pass

    def get_country_code(self):
        pass

    def get_state(self):
        pass

    def get_free_field_1(self):
        pass

    def get_free_field_2(self):
        pass

    def get_free_field_3(self):
        pass

    def get_free_field_4(self):
        pass

    def get_free_field_5(self):
        pass

    def get_free_field_6(self):
        pass

    def get_free_field_7(self):
        pass

    def get_free_field_8(self):
        pass

    def get_free_field_9(self):
        pass

    def get_free_field_10(self):
        pass

    def get_sms_id(self):
        pass

    def get_status(self):
        pass

    def get_password(self):
        pass

    def get_invoice_group(self):
        pass

    def get_city(self):
        pass

    def get_our_supplier_number_at_customer(self):
        pass

    def get_county_id(self):
        pass

    def get_place(self):
        pass

    def get_ean_location(self):
        pass

    def get_rail_station(self):
        pass

    def get_standard_point_location_code(self):
        pass

    def get_error_message_if_status_12(self):
        pass