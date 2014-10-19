from ckan import plugins
from ckan.logic.schema import (
    default_create_package_schema,
    default_update_package_schema,
    default_show_package_schema,
)

ignore_missing = plugins.toolkit.get_validator('ignore_missing')
convert_to_extras = plugins.toolkit.get_converter('convert_to_extras')
convert_from_extras = plugins.toolkit.get_converter('convert_from_extras')
is_positive_integer = plugins.toolkit.get_validator('is_positive_integer')


def package_create_schema():
    schema = default_create_package_schema()
    schema.update({
        'frequency_time_modifier': [ignore_missing, unicode,
                                    convert_to_extras],
        'frequency_count': [ignore_missing, unicode, convert_to_extras],
        'frequency_update_period': [ignore_missing, unicode,
                                    convert_to_extras],
        'frequency_period': [ignore_missing, unicode, convert_to_extras],
        # frequency is constructed from the other frequency_ fields
        'frequency': [ignore_missing],

        'retention_count': [ignore_missing, is_positive_integer,
                            convert_to_extras],
        'retention_period': [ignore_missing, unicode, convert_to_extras],
        'delivery_unit': [ignore_missing, unicode, convert_to_extras],
        'service': [ignore_missing, unicode, convert_to_extras],
    })
    return schema


def package_update_schema():
    schema = default_update_package_schema()
    schema.update({
        'frequency_time_modifier': [ignore_missing, unicode,
                                    convert_to_extras],
        'frequency_count': [ignore_missing, unicode, convert_to_extras],
        'frequency_update_period': [ignore_missing, unicode,
                                    convert_to_extras],
        'frequency_period': [ignore_missing, unicode, convert_to_extras],
        # frequency is constructed from the other frequency_ fields
        'frequency': [ignore_missing],

        'retention_count': [ignore_missing, is_positive_integer,
                            convert_to_extras],
        'retention_period': [ignore_missing, unicode, convert_to_extras],
        'delivery_unit': [ignore_missing, unicode, convert_to_extras],
        'service': [ignore_missing, unicode, convert_to_extras],
    })
    return schema


def package_show_schema():
    schema = default_show_package_schema()
    schema.update({
        'frequency_time_modifier': [convert_from_extras, ignore_missing,
                                    unicode],
        'frequency_count': [convert_from_extras, ignore_missing],
        'frequency_update_period': [convert_from_extras, ignore_missing],
        'frequency_period': [convert_from_extras, ignore_missing],

        # frequency is constructed from the other frequency_ fields
        'frequency': [collate_frequency_fields, ignore_missing],

        'retention_count': [convert_from_extras, ignore_missing,
                            is_positive_integer],
        'retention_period': [convert_from_extras, ignore_missing],
        'delivery_unit': [convert_from_extras, ignore_missing],
        'service': [convert_from_extras, ignore_missing],
    })
    return schema


def collate_frequency_fields(key, converted_data, errors, context):
    '''fetches the extras from the frequency fields and joins them into
       the single 'frequency' field
    '''
    keys = ['frequency_time_modifier', 'frequency_count',
            'frequency_update_period', 'frequency_period']

    # convert all the extras from
    # ('extras', <int>, 'key'): 'frequency_count'
    # ('extras', <int>, 'value'): '10'
    # format into a dict
    extras = {}
    for k, v in converted_data.iteritems():
        if k[0] == 'extras' and k[-1] == 'key':
            extras[v] = converted_data[k[0], k[1], 'value']

    converted_data['frequency', ] = ' '.join([extras.get(k, '') for k in keys])
