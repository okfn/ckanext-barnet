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
        'frequency_count': [ignore_missing, convert_to_extras],
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
        'next_update': [ignore_missing, unicode, convert_to_extras],
        'review_date': [ignore_missing, unicode, convert_to_extras],
        'coverage_start_date': [ignore_missing, unicode, convert_to_extras],
        'coverage_end_date': [ignore_missing, unicode, convert_to_extras],
    })
    return schema


def package_update_schema():
    schema = default_update_package_schema()
    schema.update({
        'frequency_time_modifier': [ignore_missing, unicode,
                                    convert_to_extras],
        'frequency_count': [ignore_missing, convert_to_extras],
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
        'next_update': [ignore_missing, unicode, convert_to_extras],
        'review_date': [ignore_missing, unicode, convert_to_extras],
        'coverage_start_date': [ignore_missing, unicode, convert_to_extras],
        'coverage_end_date': [ignore_missing, unicode, convert_to_extras],
    })
    return schema


def package_show_schema():
    schema = default_show_package_schema()
    schema.update({
        'frequency_time_modifier': [convert_from_extras, ignore_missing,
                                    unicode],
        'frequency_count': [convert_from_extras, ignore_missing,
                            is_positive_integer],
        'frequency_update_period': [convert_from_extras, ignore_missing],
        'frequency_period': [convert_from_extras, ignore_missing],

        # frequency is constructed from the other frequency_ fields
        'frequency': [collate_frequency_fields, ignore_missing],

        'retention_count': [convert_from_extras, ignore_missing,
                            is_positive_integer],
        'retention_period': [convert_from_extras, ignore_missing],
        'delivery_unit': [convert_from_extras, ignore_missing],
        'service': [convert_from_extras, ignore_missing],
        'next_update': [convert_from_extras, ignore_missing],
        'review_date': [convert_from_extras, ignore_missing],
        'coverage_start_date': [convert_from_extras, ignore_missing],
        'coverage_end_date': [convert_from_extras, ignore_missing],
    })
    return schema


def collate_frequency_fields(key, converted_data, errors, context):
    '''frequency is just freuqency_update_period if it exists
    otherwise it is 'Every {0} {1}'.format(frequency_count, frequency_perdiod
    '''
    # convert all the extras from
    # ('extras', <int>, 'key'): 'frequency_count'
    # ('extras', <int>, 'value'): '10'
    # format into a dict
    extras = {}
    for k, v in converted_data.iteritems():
        if k[0] == 'extras' and k[-1] == 'key':
            extras[v] = converted_data[k[0], k[1], 'value']
    option_one = extras.get('frequency_update_period')
    option_two = extras.get('frequency_period')

    if option_one:
        converted_data['frequency', ] = option_one
    elif option_two:
        converted_data['frequency', ] = ' '.join([
            'Every',
            extras.get('frequency_count', ''),
            option_two
        ])
    else:
        converted_data['frequency', ] = ''
