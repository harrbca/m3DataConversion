from transformers.crs610_add_transformer import CRS610AddTransformer

class BWLCRS610AddTransformer(CRS610AddTransformer):

    def get_customer_template(self):
        match self._item.get('BBRAN'):
            case 'SAS':
                return "Z000BWLSAS"
            case 'REG':
                return "Z000BWLREG"
            case 'CAL':
                return "Z000BWLCAL"
            case 'EDM':
                return "Z000BWLEDM"
            case 'VAN':
                return "Z000BWLVAN"
            case 'WIN':
                return "Z000BWLWIN"
            case 'TOR':
                return "Z000BWLTOR"
            case 'POR':
                return "Z000WANPOR"
            case 'SPO':
                return "Z000WANSPO"
            case 'TUK':
                return "Z000WANTUK"
            case 'ZSE':
                return "Z000WANXSE"
            case _:
                return None

    def get_customer_number(self):
        match self._item.get('schemaName'):
            case 'BWL':
                return f"1{self._item.get('accountNumber')}"
            case 'WAN':
                return f"2{self._item.get('accountNumber')}"
            case _:
                return None

    def get_country_code(self):
        # if a canadian state, return CA
        # otherwise return US
        if self._item.get('BSTATE') in ['AB', 'BC', 'MB', 'NB', 'NL', 'NS', 'NT', 'NU', 'ON', 'PE', 'QC', 'SK', 'YT', 'PQ']:
            return "CA"
        else:
            return "US"

    def get_language_code(self):
        return "GB"

    def get_customer_name(self):
        return self._item.get('BNAME').strip()

    def get_customer_address_1(self):
        # if the address is empty, then return the address 2
        # otherwise return the address 1
        if self._item.get('BADDR1').strip() == "":
            if self._item.get('BADDR2').strip != "":
                return self._item.get('BADDR2').strip()
            else:
                return "."
        return self._item.get('BADDR1').strip()

    def get_customer_address_2(self):
        # if address 1 was empty, then address 2 was already returned, send nothing
        # otherwise return the address 2
        if self._item.get('BADDR1').strip() == "":
            return None
        return (
            self._item.get('BADDR2').strip())

    def get_city(self):
        if(self._item.get('schemaName') == 'BWL'):
            # return only the first 23 characters of the city name and then strip it
            # to remove any trailing spaces
            return (self._item.get('BCITY'))[:23].strip()

        else:
            # return the full city name and then strip it to remove any trailing spaces
            return self._item.get('BCITY').strip()

    def get_state(self):
        return self._item.get('BSTATE').strip()

    def get_postal_code(self):
        # if bzip1 and bzip2 are both not zero, then return them as a string
        # otherwise return bzip1
        if self._item.get('BZIP1') != 0 and self._item.get('BZIP2') != 0:
            return f"{self._item.get('BZIP1')}-{self._item.get('BZIP2')}"
        elif self._item.get('BZIP1') != 0:
            return f"{self._item.get('BZIP1')}"
        else:
            # return the 7 right most characters of bcity
            return self._item.get('BCITY')[-7:].strip()

    def get_status(self):
        return "20"

    def get_phone_number(self):
        # if the phone number is not empty, return it
        # otherwise return the fax number
        if self._item.get('BPHONB') != 0:
           return self.format_phone_number(self._item.get('BPHONB'))
        else:
            return None

    def get_fax_number(self):
        # if the fax number is not empty, return it
        # otherwise return the phone number
        if self._item.get('BPHONH'):
            return self.format_phone_number(self._item.get('BPHONH'))
        else:
            return None

    def format_phone_number(self, number):
        # if the length of the number is 10, then format is a phone number
        # otherwise return the phone number
        number = str(number)
        if len(number) == 10:
            return f"({number[:3]}) {number[3:6]}-{number[6:]}"
        else:
            return number.strip()