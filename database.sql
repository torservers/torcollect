CREATE TABLE Server (
    SRV_ID SERIAL,
    SRV_IP VARCHAR(39) UNIQUE,
    SRV_NAME VARCHAR(64),
    PRIMARY KEY (SRV_ID)
);

CREATE TABLE Login (
    LGI_ID SERIAL,
    LGI_SRV_ID INTEGER,
    LGI_AUTHTYPE INTEGER,
    LGI_SSHPORT INTEGER,
    LGI_USER VARCHAR(256),
    LGI_PASSWORD VARCHAR(256),
    LGI_KEYFILE BYTEA DEFAULT NULL,
    PRIMARY KEY (LGI_ID)
);

CREATE TABLE Bridge(
    BRG_ID SERIAL,
    BRG_SRV_ID INTEGER,
    BRG_NR INTEGER,
    BRG_IP VARCHAR(39),
    PRIMARY KEY (BRG_ID)
);

CREATE TABLE Report(
    REP_ID SERIAL,
    REP_BRG_ID INTEGER,
    REP_DATE DATE,
    REP_PORT INTEGER,
    REP_TRAFFIC_SENT BIGINT,
    REP_TRAFFIC_RECEIVED BIGINT,
    PRIMARY KEY (REP_ID)
);

CREATE TABLE CountryReport(
    CRP_REP_ID INTEGER,
    CRP_CCO_ID INTEGER,
    CRP_USERS INTEGER,
    PRIMARY KEY (CRP_REP_ID, CRP_CCO_ID)
);

CREATE TABLE TransportReport(
    TRP_REP_ID INTEGER,
    TRP_TRA_ID INTEGER,
    TRP_USERS INTEGER,
    PRIMARY KEY (TRP_REP_ID, TRP_TRA_ID)
);

CREATE TABLE CountryCode(
    CCO_ID SERIAL,
    CCO_SHORT VARCHAR(2),
    CCO_LONG VARCHAR(64),
    PRIMARY KEY (CCO_ID)
);

CREATE TABLE Transport(
    TRA_ID SERIAL,
    TRA_NAME VARCHAR(64),
    PRIMARY KEY (TRA_ID)
);

CREATE TABLE DisclosureTo(
    DSC_BRG_ID INTEGER,
    DSC_ORG_ID INTEGER,
    PRIMARY KEY (DSC_BRG_ID, DSC_ORG_ID)
);

CREATE TABLE Organization(
    ORG_ID SERIAL,
    ORG_NAME VARCHAR(256),
    PRIMARY KEY (ORG_ID)
);

ALTER TABLE Login ADD CONSTRAINT FK_LGI_SRV
    FOREIGN KEY (LGI_SRV_ID) REFERENCES Server (SRV_ID) ON DELETE CASCADE;

ALTER TABLE Bridge ADD CONSTRAINT FK_BRG_SRV
    FOREIGN KEY (BRG_SRV_ID) REFERENCES Server (SRV_ID) ON DELETE CASCADE;

ALTER TABLE Report ADD CONSTRAINT FK_REP_BRG
    FOREIGN KEY (REP_BRG_ID) REFERENCES Bridge (BRG_ID) ON DELETE CASCADE;

ALTER TABLE CountryReport ADD CONSTRAINT FK_CRP_REP
    FOREIGN KEY (CRP_REP_ID) REFERENCES Report (REP_ID) ON DELETE CASCADE;

ALTER TABLE CountryReport ADD CONSTRAINT FK_CRP_CCO
    FOREIGN KEY (CRP_CCO_ID) REFERENCES CountryCode (CCO_ID) ON DELETE CASCADE;

ALTER TABLE TransportReport ADD CONSTRAINT FK_TRP_REP
    FOREIGN KEY (TRP_REP_ID) REFERENCES Report (REP_ID) ON DELETE CASCADE;

ALTER TABLE TransportReport ADD CONSTRAINT FK_TRP_TRA
    FOREIGN KEY (TRP_TRA_ID) REFERENCES Transport (TRA_ID) ON DELETE CASCADE;

ALTER TABLE DisclosureTo ADD CONSTRAINT FK_DSC_BRG
    FOREIGN KEY (DSC_BRG_ID) REFERENCES Bridge (BRG_ID) ON DELETE CASCADE;

ALTER TABLE DisclosureTo ADD CONSTRAINT FK_DSC_ORG
    FOREIGN KEY (DSC_ORG_ID) REFERENCES Organization (ORG_ID) ON DELETE CASCADE;



INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('A1',E'Anonymous Proxy', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('A2',E'Satellite Provider', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('O1',E'Other Country', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('AD',E'Andorra', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('AE',E'United Arab Emirates', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('AF',E'Afghanistan', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('AG',E'Antigua and Barbuda', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('AI',E'Anguilla', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('AL',E'Albania', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('AM',E'Armenia', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('AO',E'Angola', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('AP',E'Asia/Pacific Region', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('AQ',E'Antarctica', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('AR',E'Argentina', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('AS',E'American Samoa', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('AT',E'Austria', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('AU',E'Australia', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('AW',E'Aruba', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('AX',E'Aland Islands', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('AZ',E'Azerbaijan', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('BA',E'Bosnia and Herzegovina', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('BB',E'Barbados', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('BD',E'Bangladesh', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('BE',E'Belgium', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('BF',E'Burkina Faso', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('BG',E'Bulgaria', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('BH',E'Bahrain', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('BI',E'Burundi', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('BJ',E'Benin', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('BL',E'Saint Bartelemey', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('BM',E'Bermuda', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('BN',E'Brunei Darussalam', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('BO',E'Bolivia', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('BQ',E'Bonaire, Saint Eustatius and Saba', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('BR',E'Brazil', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('BS',E'Bahamas', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('BT',E'Bhutan', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('BV',E'Bouvet Island', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('BW',E'Botswana', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('BY',E'Belarus', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('BZ',E'Belize', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('CA',E'Canada', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('CC',E'Cocos (Keeling) Islands', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('CD',E'Congo, The Democratic Republic of the', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('CF',E'Central African Republic', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('CG',E'Congo', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('CH',E'Switzerland', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('CI',E'Cote d''Ivoire', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('CK',E'Cook Islands', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('CL',E'Chile', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('CM',E'Cameroon', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('CN',E'China', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('CO',E'Colombia', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('CR',E'Costa Rica', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('CU',E'Cuba', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('CV',E'Cape Verde', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('CW',E'Curacao', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('CX',E'Christmas Island', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('CY',E'Cyprus', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('CZ',E'Czech Republic', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('DE',E'Germany', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('DJ',E'Djibouti', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('DK',E'Denmark', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('DM',E'Dominica', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('DO',E'Dominican Republic', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('DZ',E'Algeria', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('EC',E'Ecuador', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('EE',E'Estonia', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('EG',E'Egypt', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('EH',E'Western Sahara', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('ER',E'Eritrea', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('ES',E'Spain', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('ET',E'Ethiopia', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('EU',E'Europe', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('FI',E'Finland', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('FJ',E'Fiji', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('FK',E'Falkland Islands (Malvinas)', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('FM',E'Micronesia, Federated States of', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('FO',E'Faroe Islands', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('FR',E'France', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('GA',E'Gabon', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('GB',E'United Kingdom', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('GD',E'Grenada', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('GE',E'Georgia', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('GF',E'French Guiana', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('GG',E'Guernsey', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('GH',E'Ghana', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('GI',E'Gibraltar', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('GL',E'Greenland', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('GM',E'Gambia', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('GN',E'Guinea', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('GP',E'Guadeloupe', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('GQ',E'Equatorial Guinea', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('GR',E'Greece', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('GS',E'South Georgia and the South Sandwich Islands', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('GT',E'Guatemala', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('GU',E'Guam', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('GW',E'Guinea-Bissau', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('GY',E'Guyana', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('HK',E'Hong Kong', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('HM',E'Heard Island and McDonald Islands', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('HN',E'Honduras', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('HR',E'Croatia', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('HT',E'Haiti', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('HU',E'Hungary', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('ID',E'Indonesia', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('IE',E'Ireland', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('IL',E'Israel', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('IM',E'Isle of Man', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('IN',E'India', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('IO',E'British Indian Ocean Territory', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('IQ',E'Iraq', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('IR',E'Iran, Islamic Republic of', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('IS',E'Iceland', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('IT',E'Italy', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('JE',E'Jersey', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('JM',E'Jamaica', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('JO',E'Jordan', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('JP',E'Japan', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('KE',E'Kenya', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('KG',E'Kyrgyzstan', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('KH',E'Cambodia', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('KI',E'Kiribati', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('KM',E'Comoros', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('KN',E'Saint Kitts and Nevis', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('KP',E'Korea, Democratic People''s Republic of', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('KR',E'Korea, Republic of', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('KW',E'Kuwait', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('KY',E'Cayman Islands', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('KZ',E'Kazakhstan', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('LA',E'Lao People''s Democratic Republic', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('LB',E'Lebanon', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('LC',E'Saint Lucia', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('LI',E'Liechtenstein', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('LK',E'Sri Lanka', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('LR',E'Liberia', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('LS',E'Lesotho', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('LT',E'Lithuania', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('LU',E'Luxembourg', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('LV',E'Latvia', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('LY',E'Libyan Arab Jamahiriya', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('MA',E'Morocco', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('MC',E'Monaco', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('MD',E'Moldova, Republic of', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('ME',E'Montenegro', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('MF',E'Saint Martin', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('MG',E'Madagascar', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('MH',E'Marshall Islands', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('MK',E'Macedonia', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('ML',E'Mali', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('MM',E'Myanmar', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('MN',E'Mongolia', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('MO',E'Macao', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('MP',E'Northern Mariana Islands', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('MQ',E'Martinique', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('MR',E'Mauritania', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('MS',E'Montserrat', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('MT',E'Malta', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('MU',E'Mauritius', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('MV',E'Maldives', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('MW',E'Malawi', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('MX',E'Mexico', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('MY',E'Malaysia', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('MZ',E'Mozambique', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('NA',E'Namibia', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('NC',E'New Caledonia', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('NE',E'Niger', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('NF',E'Norfolk Island', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('NG',E'Nigeria', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('NI',E'Nicaragua', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('NL',E'Netherlands', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('NO',E'Norway', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('NP',E'Nepal', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('NR',E'Nauru', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('NU',E'Niue', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('NZ',E'New Zealand', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('OM',E'Oman', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('PA',E'Panama', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('PE',E'Peru', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('PF',E'French Polynesia', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('PG',E'Papua New Guinea', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('PH',E'Philippines', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('PK',E'Pakistan', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('PL',E'Poland', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('PM',E'Saint Pierre and Miquelon', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('PN',E'Pitcairn', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('PR',E'Puerto Rico', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('PS',E'Palestinian Territory', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('PT',E'Portugal', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('PW',E'Palau', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('PY',E'Paraguay', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('QA',E'Qatar', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('RE',E'Reunion', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('RO',E'Romania', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('RS',E'Serbia', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('RU',E'Russian Federation', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('RW',E'Rwanda', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('SA',E'Saudi Arabia', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('SB',E'Solomon Islands', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('SC',E'Seychelles', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('SD',E'Sudan', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('SE',E'Sweden', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('SG',E'Singapore', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('SH',E'Saint Helena', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('SI',E'Slovenia', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('SJ',E'Svalbard and Jan Mayen', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('SK',E'Slovakia', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('SL',E'Sierra Leone', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('SM',E'San Marino', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('SN',E'Senegal', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('SO',E'Somalia', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('SR',E'Suriname', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('SS',E'South Sudan', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('ST',E'Sao Tome and Principe', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('SV',E'El Salvador', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('SX',E'Sint Maarten', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('SY',E'Syrian Arab Republic', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('SZ',E'Swaziland', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('TC',E'Turks and Caicos Islands', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('TD',E'Chad', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('TF',E'French Southern Territories', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('TG',E'Togo', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('TH',E'Thailand', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('TJ',E'Tajikistan', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('TK',E'Tokelau', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('TL',E'Timor-Leste', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('TM',E'Turkmenistan', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('TN',E'Tunisia', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('TO',E'Tonga', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('TR',E'Turkey', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('TT',E'Trinidad and Tobago', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('TV',E'Tuvalu', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('TW',E'Taiwan', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('TZ',E'Tanzania, United Republic of', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('UA',E'Ukraine', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('UG',E'Uganda', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('UM',E'United States Minor Outlying Islands', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('US',E'United States', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('UY',E'Uruguay', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('UZ',E'Uzbekistan', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('VA',E'Holy See (Vatican City State)', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('VC',E'Saint Vincent and the Grenadines', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('VE',E'Venezuela', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('VG',E'Virgin Islands, British', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('VI',E'Virgin Islands, U.S.', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('VN',E'Vietnam', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('VU',E'Vanuatu', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('WF',E'Wallis and Futuna', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('WS',E'Samoa', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('YE',E'Yemen', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('YT',E'Mayotte', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('ZA',E'South Africa', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('ZM',E'Zambia', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('ZW',E'Zimbabwe', DEFAULT);
INSERT INTO CountryCode (CCO_SHORT, CCO_LONG, CCO_ID) VALUES ('??',E'Unknown', DEFAULT);
