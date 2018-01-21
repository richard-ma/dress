def command_sed_helper(source, target, filename, ignore_case=False):
    return "sed -i \"s/%s/%s/%sg\" %s" % (
            source,
            target,
            'I' if ignore_case else '',
            filename)
