from msgraph import GraphServiceClient

from azure.identity import InteractiveBrowserCredential,DefaultAzureCredential
import json
import csv


# credential = DefaultAzureCredential()
# try:

#     # Check if given credential can get token successfully.
#     credential.get_token("https://management.azure.com/.default")
# except Exception as ex:
#     # Fall back to InteractiveBrowserCredential in case DefaultAzureCredential not work
#     credential = InteractiveBrowserCredential()
credential = InteractiveBrowserCredential()
graph_client = GraphServiceClient(credential, scopes=['https://graph.microsoft.com/.default'])
file_name = 'group_info'

async def get_my_members_of():
    group_members = {}
    memberships = await graph_client.me.member_of.get()
    count = 0
    if memberships and memberships.value:
        for membership in memberships.value:
            print(count)
            count += 1
            print(membership.id)
            group_members[membership.id] = (membership.display_name, [])
            result = await graph_client.groups.by_group_id(membership.id).transitive_member_of.get()
            if result and result.value:
                for group in result.value:
                    group_members[membership.id][1].append((group.id, group.display_name))
            while result is not None and result.odata_next_link is not None:
                result = await graph_client.groups.by_group_id(membership.id).transitive_member_of.with_url(result.odata_next_link).get()
                if result and result.value:
                    for group in result.value:
                        group_members[membership.id][1].append((group.id, group.display_name))
                
    while memberships is not None and memberships.odata_next_link is not None:
            memberships = await graph_client.me.member_of.with_url(memberships.odata_next_link).get()
            if memberships and memberships.value:
                for membership in memberships.value:
                    print(count)
                    count += 1
                    print(membership.id)
                    group_members[membership.id] = (membership.display_name, [])
                    result = await graph_client.groups.by_group_id(membership.id).transitive_member_of.get()
                    if result and result.value:
                        for group in result.value:
                            group_members[membership.id][1].append((group.id, group.display_name))
                    while result is not None and result.odata_next_link is not None:
                        result = await graph_client.groups.by_group_id(membership.id).transitive_member_of.with_url(result.odata_next_link).get()
                        if result and result.value:
                            for group in result.value:
                                group_members[membership.id][1].append((group.id, group.display_name))
    return group_members



def export_group_info_to_json(group_info, filename):
    with open(filename, 'w') as json_file:
        json.dump(group_info, json_file, indent=4)


def export_group_info_summary_to_csv(group_info, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(['Group ID', 'Display Name', 'Members Count'])
        
        # Write data for each group
        for group_id, (display_name, members) in group_info.items():
            writer.writerow([group_id, display_name, len(members)])

import asyncio

# asyncio.run(get_memberships())

group_members = asyncio.run(get_my_members_of())

ordered_group_members = dict(sorted(group_members.items(), key=lambda item: len(item[1][1]), reverse=True))

export_group_info_to_json(ordered_group_members, file_name+'.json')
export_group_info_summary_to_csv(ordered_group_members, file_name+'.csv')



# asyncio.run(get_data())

